from logging import getLogger
from typing import Iterator, Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.strategy_options import joinedload, selectinload
from sqlalchemy.types import String
from sqlalchemy.sql.expression import Select, delete, func, insert, select

from phystool.config import config
from phystool.helper import greptex, progress_bar
from phystool.pdbfile import PDBFile
from phystool.physql import physql_db
from phystool.physql.models import PDBRecord, PDBType, Category, Tag, tag_relation
from phystool.tags import Tags
from phystool.__version__ import __version__

logger = getLogger(__name__)


def stats() -> dict[str, str | int | Sequence[str] | dict[str, list[str]]]:
    with physql_db() as session:
        return {
            "path": str(config.db.DB_DIR),
            "records_number": session.scalar(func.count(PDBRecord.id)),
            "valid_types": session.scalars(select(PDBType.name)).all(),
            "valid_tags": Tags.manager.tags.data,
            "version": str(__version__),
        }


def consolidate() -> None:
    """
    Wrapper function around `create_sql_database()' that prints a minimalistic
    progress bar in the terminal
    """
    _message = ""
    for i, n, message in create_sql_database():
        if _message != message:
            _message = message
            print()
        progress_bar(n, i, 20, f"{message:<30} |")
    print()


def create_sql_database() -> Iterator[tuple[int, int, str]]:
    """Create the SQL database by analysing all '.tex' and related '.json' files"""
    pdb_type_map = {
        name: PDBType(name=name, standalone=standalone)
        for name, (_, standalone) in config.db.PDB_TYPES.items()
    }

    tags = Tags({})
    tag_map: dict[tuple[str, str], Tag] = {}
    category_map: dict[str, Category] = {}
    pdb_records: list[PDBRecord] = []
    reference_map: dict[UUID, list[UUID]] = {}

    i = 0
    tex_files = list(config.db.DB_DIR.glob("*.tex"))
    n = len(tex_files) - 1
    for i, tex_file in enumerate(tex_files):
        yield i, n, "Updating '.json' and '.pdf' files"
        try:
            pdb_file = PDBFile.from_file(tex_file)
        except ValueError as e:
            logger.error(e)
            continue
        pdb_file.compile(False)
        pdb_file.save()

        tag_set: set[Tag] = set()
        if not pdb_file.tags:
            logger.warning(f"{pdb_file!r} is untagged")
        else:
            tags += pdb_file.tags
            for category_name, pdbfile_tags in pdb_file.tags:
                if not (category := category_map.get(category_name, None)):
                    category = Category(name=category_name)
                    category_map[category_name] = category

                for tag_name in pdbfile_tags:
                    if not (tag := tag_map.get((category_name, tag_name), None)):
                        tag = Tag(name=tag_name, category=category)
                        tag_map[(category_name, tag_name)] = tag
                    tag_set.add(tag)

        pdb_records.append(
            PDBRecord(
                uuid=pdb_file.uuid,
                title=pdb_file.title,
                pdb_type=pdb_type_map[pdb_file.pdb_type],
                tag_set=tag_set,
            )
        )
        if refs := pdb_file.references:
            reference_map[pdb_file.uuid] = refs

    yield 0, 0, "Creating SQL database"
    physql_db.reset()
    with physql_db() as session:
        session.add_all(category_map.values())
        session.add_all(tag_map.values())
        session.add_all(pdb_type_map.values())
        session.add_all(pdb_records)

    # Manage references and inherited tags
    with physql_db() as session:
        pdb_record_map = {
            pdb_record.uuid: pdb_record
            for pdb_record in session.scalars(select(PDBRecord))
        }
        for pdb_record_uuid, reference_uuids in reference_map.items():
            tmp_record = pdb_record_map[pdb_record_uuid]
            tmp_record.using_set = {
                pdb_record_map[reference_uuid] for reference_uuid in reference_uuids
            }
            for reference_uuid in reference_uuids:
                pdb_record_map[reference_uuid].tag_set.update(tmp_record.tag_set)

    Tags.manager.reload_from_db()
    if tags != Tags.manager.tags:
        physql_db.reset()
        yield 1, 1, "SQL creation failed"
        raise ValueError(f"SQL creation failed")

    yield 0, 0, "Removing extraneous files"
    for f in config.db.DB_DIR.glob("*"):
        if f.suffix in [".aux", ".log"]:
            f.unlink()
        elif (
            f.suffix in [".json", ".pdf", ".pty"]
            and not f.with_suffix(".tex").is_file()
        ):
            logger.info(f"rm {f}")

    yield 1, 1, "Consolidation completed"


def _default_query_for_filter() -> Select[tuple[PDBRecord]]:
    return (
        select(PDBRecord)
        .options(joinedload(PDBRecord.pdb_type))
        .options(selectinload(PDBRecord.tag_set))
        .options(selectinload(PDBRecord.using_set))
    )


def filter_pdb_files(
    query: str,
    uuid_bit: str,
    pdb_types: set[str],
    selected_tags: Tags,
    excluded_tags: Tags,
) -> list[PDBFile]:
    """
    Returns a list of PDBFile that match search criteria

    :param query: string that should appear in the '.tex' file
    :param uuid_bit: string that should match part of a uuid
    :param pdb_type_set: restrain search only to those file types
    :param selected_tags: restrain search to the PDBFiles tagged with any of the
        selected_tags
    :param excluded_tags: exclude PDBFiles tagged with any of the
        excluded_tags
    """
    qs = _default_query_for_filter()
    if query:
        qs = qs.filter(PDBRecord.uuid.in_(greptex(query, config.db.DB_DIR, False)))
    if pdb_types:
        qs = qs.filter(PDBType.name.in_(pdb_types)).join(PDBType)
    if uuid_bit:
        qs = qs.filter(func.cast(PDBRecord.uuid, String).like(f"%{uuid_bit}%"))
    with physql_db() as session:
        return sorted(
            [
                PDBFile.from_record(pdb_record)
                for pdb_record in session.scalars(qs)
                if (
                    pdb_record.tags.with_overlap(selected_tags)
                    and pdb_record.tags.without_overlap(excluded_tags)
                )
            ],
            reverse=True,
        )


def filter_pdb_files_by_uuids(uuids: list[UUID]) -> list[PDBFile]:
    with physql_db() as session:
        return [
            PDBFile.from_record(pdb_record)
            for pdb_record in session.scalars(
                _default_query_for_filter().filter(PDBRecord.uuid.in_(uuids))
            )
        ]


def update_pdb_file(pdb_file: PDBFile) -> None:
    pdb_file.save()
    with physql_db() as session:
        pdb_type = session.execute(
            select(PDBType).filter_by(name=pdb_file.pdb_type)
        ).scalar_one()
        using = session.scalars(
            select(PDBRecord).filter(PDBRecord.uuid.in_(pdb_file.references))
        )
        if pdb_record := session.execute(
            select(PDBRecord).filter_by(uuid=pdb_file.uuid)
        ).scalar():
            pdb_record.title = pdb_file.title
            pdb_record.pdb_type = pdb_type
            pdb_record.using_set = set(using)
            logger.info(f"Successfully updated {pdb_file!r}")
        else:
            session.add(
                PDBRecord(
                    uuid=pdb_file.uuid,
                    title=pdb_file.title,
                    pdb_type=pdb_type,
                    using_set=set(using),
                )
            )
            logger.info(f"Successfully created {pdb_file!r}")


def remove_pdb_files(uuids: list[UUID]) -> None:
    """
    Remove all files related to the PDBFiles. If the database is managed by
    git, the files can be recovered. The PDBRecords are also deleted.
    """
    with physql_db() as session:
        session.execute(delete(PDBRecord).filter(PDBRecord.uuid.in_(uuids)))

    for uuid in uuids:
        for fname in config.db.DB_DIR.glob(f"{uuid}*"):
            logger.info(f"Removing {fname}")
            fname.unlink()


def create_new_tag(category_name: str, tag_name: str) -> None:
    # TODO: need to test this is the GUI
    try:
        with physql_db() as session:
            if not (
                category := session.scalars(
                    select(Category).filter_by(name=category_name)
                ).one_or_none()
            ):
                category = Category(name=category_name)
                session.add(category)
            session.add(Tag(name=tag_name, category=category))
            try:
                Tags.manager.tags.data[category_name].append(tag_name)
            except:
                Tags.manager.tags.data[category_name] = [tag_name]
    except IntegrityError:
        logger.warning(f"Can't duplicate existing tag '{category_name}: {tag_name}'")


def update_tags(
    pdb_file: PDBFile,
    session: Session,
    to_remove_ids: set[int],
    to_add_ids: set[int],
) -> None:
    """Update the tags, both in the SQL database and in the .json file"""
    if to_delete := (pdb_file.tags.as_ids() & to_remove_ids):
        session.execute(
            delete(tag_relation).filter(
                tag_relation.c.tag_id.in_(to_delete),
                tag_relation.c.pdb_record_id == pdb_file.id,
            )
        )
        pdb_file.tags -= Tags.manager.from_ids(to_delete)
    if to_create := (to_add_ids - pdb_file.tags.as_ids()):
        session.execute(
            insert(tag_relation).values(
                [
                    {"pdb_record_id": pdb_file.id, "tag_id": tag_id}
                    for tag_id in to_create
                ]
            )
        )
        pdb_file.tags += Tags.manager.from_ids(to_create)
    pdb_file.save()
