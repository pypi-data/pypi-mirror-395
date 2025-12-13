from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logging import getLogger
from pathlib import Path
from sys import exit
from uuid import UUID

from phystool.config import config
from phystool.latex import PdfLatex


logger = getLogger(__name__)


def _default(args) -> None:
    if args.list_tags:
        from phystool.tags import Tags

        Tags.manager.tags.display()
    elif args.new_pdb_filename:
        print(config.new_pdb_filename())
    elif args.db_dir:
        print(config.db.DB_DIR)
    elif args.consolidate:
        from phystool.physql.metadata import consolidate

        consolidate()
    elif args.stats:
        from phystool.physql.metadata import stats
        from json import dumps

        print(dumps(stats(), indent=4))
    elif args.git:
        from phystool.physgit import run_git_in_terminal

        run_git_in_terminal()


def _search(args) -> None:
    from phystool.physql.metadata import filter_pdb_files
    from phystool.tags import Tags

    for pdb_file in filter_pdb_files(
        query=args.query,
        uuid_bit=args.uuid,
        pdb_types=args.pdb_types,
        selected_tags=Tags.manager.from_ids(args.tags),
        excluded_tags=Tags({}),
    ):
        print(pdb_file)


def _pdbfile(args) -> None:
    from phystool.pdbfile import PDBFile

    try:
        pdb_file = PDBFile.from_file(args.uuid)
    except ValueError as e:
        logger.error(e)
        exit(1)

    if args.compile:
        if not pdb_file.compile(True):
            exit(1)
    elif args.zip:
        pdb_file.zip()
    elif args.cat:
        pdb_file.bat()
    elif args.update:
        from phystool.physql.metadata import update_pdb_file

        update_pdb_file(pdb_file)
        print(pdb_file)
    elif args.remove:
        from phystool.helper import terminal_yes_no
        from phystool.physql.metadata import remove_pdb_files

        pdb_file.bat()
        if terminal_yes_no("Remove files?"):
            remove_pdb_files([pdb_file.uuid])


def _tags(args) -> None:
    from phystool.physql import physql_db
    from phystool.physql.metadata import filter_pdb_files_by_uuids, update_tags

    if pdb_files := filter_pdb_files_by_uuids([args.uuid]):
        pdb_file = pdb_files[0]
        with physql_db() as session:
            update_tags(
                pdb_file,
                session,
                to_remove_ids=args.remove,
                to_add_ids=args.add,
            )
            if args.list:
                pdb_file.tags.display()
            else:
                print(pdb_file)


def _pdflatex(args) -> None:
    from phystool.latex import LatexLogParser, LogFileMessage, PdfLatex
    from phystool.helper import texfile_to_symlink

    if args.raw_log:
        LogFileMessage.toggle_verbose_mode()

    if not args.filename.exists():
        logger.error(f"'{args.filename}' not found")
        exit(1)
    elif args.filename.suffix == ".log" or args.logtex:
        if not args.filename.with_suffix(".log").exists():
            args.filename = texfile_to_symlink(args.filename).with_suffix(".log")
            if not args.filename.exists():
                logger.error(f"'{args.filename}' not found")
                exit(1)
        llp = LatexLogParser(args.filename)
        llp.process()
        llp.as_log()
    else:
        pdflatex = PdfLatex(texfile_to_symlink(args.filename))
        if args.output:
            if not pdflatex.full_compile(args.output, args.can_recompile):
                exit(1)
        if args.clean:
            pdflatex.clean([".aux", ".log", ".out", ".toc"])


def _evaluation_action(args):
    from phystool.evaluation import Evaluation, load_klass_and_evaluation_data

    load_klass_and_evaluation_data()
    evaluation_uuids = Evaluation.search(
        year=args.year,
        exuuid=args.exuuid,
        evuuid=args.evuuid,
        cluuid=args.cluuid,
    )
    match args.action:
        case "display":
            for uuid in evaluation_uuids:
                Evaluation.display(uuid)
        case "list":
            for uuid in evaluation_uuids:
                print(uuid, Evaluation.all[uuid])
        case "update":
            if evaluation := Evaluation.update(args.evuuid, args.fname):
                print(evaluation)
            else:
                exit(1)
        case "create":
            if evaluation := Evaluation.create(args.fname):
                print(evaluation)
            else:
                exit(1)


def _klass_action(args):
    from phystool.evaluation import Klass, load_klass_and_evaluation_data

    load_klass_and_evaluation_data()
    klass_uuids = Klass.search(name=args.name, year=args.year)
    match args.action:
        case "display":
            for uuid in klass_uuids:
                Klass.display(uuid)
        case "list":
            for uuid in klass_uuids:
                print(uuid, Klass.all[uuid])
        case "update":
            if klass := Klass.update(
                uuid=args.cluuid,
                name=args.name,
                extra=args.extra,
                year=args.year,
            ):
                print(klass)
            else:
                exit(1)
        case "create":
            if klass := Klass.create(
                name=args.name,
                extra=args.extra,
                year=args.year,
            ):
                print(klass)
            else:
                exit(1)


def get_parser():
    parser = ArgumentParser(
        prog="phystool",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.set_defaults(func=_default)
    parser.add_argument(
        "--list-tags",
        help="Lists all possible tags",
        action="store_true",
    )
    parser.add_argument(
        "--consolidate",
        help="Consolidates the SQL database",
        action="store_true",
    )
    parser.add_argument(
        "--new-pdb-filename",
        help="Returns new PDBFile filename",
        action="store_true",
    )
    parser.add_argument(
        "--git",
        help="Commits database modifications to git",
        action="store_true",
    )
    parser.add_argument(
        "--stats",
        help="Prints information about phystool and the database",
        action="store_true",
    )
    parser.add_argument(
        "--db-dir",
        help="Prints directory which contains the PDBFile database",
        action="store_true",
    )

    sub_parser = parser.add_subparsers()
    ###########################
    # search
    ###########################
    search_parser = sub_parser.add_parser(
        "search",
        help="Search in database",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    search_parser.set_defaults(func=_search)
    search_parser.add_argument(
        "--tags",
        help="Filter by tags",
        type=lambda x: {int(i) for i in x.split(",")},
        default=set(),
    )
    search_parser.add_argument(
        "--pdb-types",
        help="Filter by types",
        type=lambda x: {
            pdb_type for pdb_type in x.split(",") if pdb_type in config.db.PDB_TYPES
        },
        default=set(),
    )
    search_parser.add_argument(
        "--uuid",
        help="Filter by uuid containing",
        default="",
    )
    search_parser.add_argument(
        "--query",
        help="Filter the search by content matching the query",
        default="",
    )

    ###########################
    # PDBFile
    ###########################
    pdbfile_parser = sub_parser.add_parser(
        "pdbfile",
        help="Act on pdbfile",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    pdbfile_parser.set_defaults(func=_pdbfile)
    pdbfile_parser.add_argument(
        "uuid",
        help="Select the PDBFile by its uuid",
        type=UUID,
    )
    pdbfile_parser.add_argument(
        "--cat",
        help="Display in terminal",
        action="store_true",
    )
    pdbfile_parser.add_argument(
        "--compile",
        help="Compile '.tex' file",
        action="store_true",
    )
    pdbfile_parser.add_argument(
        "--remove",
        help="Remove from database",
        action="store_true",
    )
    pdbfile_parser.add_argument(
        "--update",
        help="Update metadata by parsing the '.tex' file",
        action="store_true",
    )
    pdbfile_parser.add_argument(
        "--zip",
        help="Zip with its dependencies",
        action="store_true",
    )

    ###########################
    # PDBFile -> Tags
    ###########################
    sub_sub_parser = pdbfile_parser.add_subparsers()
    tags_subparser = sub_sub_parser.add_parser(
        "tags",
        help="List or edit tags for selected PDBFile",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    tags_subparser.set_defaults(func=_tags)
    tags_subparser.add_argument(
        "--add",
        help="Add tags given as a comma separated list of ids",
        type=lambda x: {int(i.strip()) for i in x.split(",")},
        default=set(),
    )
    tags_subparser.add_argument(
        "--remove",
        help="Remove tags given as a comma separated list of ids",
        type=lambda x: {int(i.strip()) for i in x.split(",")},
        default=set(),
    )
    tags_subparser.add_argument(
        "--list",
        help="List tags",
        action="store_true",
    )

    ###########################
    # PdfLatex
    ###########################
    pdflatex_parser = sub_parser.add_parser(
        "pdflatex",
        help="Compile LaTeX documents or parse logs",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    pdflatex_parser.set_defaults(func=_pdflatex)
    pdflatex_parser.add_argument(
        "filename",
        help="Path to '.tex' file",
        type=Path,
    )
    pdflatex_parser.add_argument(
        "--output",
        help="Move pdf to destination",
        type=PdfLatex.output,
    )
    pdflatex_parser.add_argument(
        "--logtex",
        help="Dislpay .log file",
        action="store_true",
    )
    pdflatex_parser.add_argument(
        "--can-recompile",
        help="Compile a second time if the log file mentions the need",
        action="store_true",
    )
    pdflatex_parser.add_argument(
        "--raw-log",
        help="Display raw error message",
        action="store_true",
    )
    pdflatex_parser.add_argument(
        "--clean",
        help="Remove auxiliary files",
        action="store_true",
    )
    if config.EVALUATION_PATH.exists():
        ###########################
        # evaluation
        ###########################
        evaluation_subparser = sub_parser.add_parser(
            "evaluation",
            help="Manage evaluations",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        evaluation_subparser.set_defaults(func=_evaluation_action)
        evaluation_subparser.add_argument(
            "action",
            help="Acts uppon evaluations",
            choices=["display", "list", "update", "create"],
        )
        evaluation_subparser.add_argument(
            "--evuuid",
            help="Evaluation UUID",
            type=UUID,
        )
        evaluation_subparser.add_argument(
            "--exuuid",
            help="Exercise UUID",
            type=UUID,
        )
        evaluation_subparser.add_argument(
            "--cluuid",
            help="Class UUID",
            type=UUID,
        )
        evaluation_subparser.add_argument(
            "--year",
            help="Scolar year",
            default=0,
            type=int,
        )
        evaluation_subparser.add_argument(
            "--fname",
            help="Evaluation file to process",
            type=Path,
        )

        ###########################
        # Klass
        ###########################
        klass_subparser = sub_parser.add_parser(
            "class",
            help="Manage classes",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        klass_subparser.set_defaults(func=_klass_action)
        klass_subparser.add_argument(
            "action",
            help="Acts uppon classes",
            choices=["display", "list", "update", "create"],
        )
        klass_subparser.add_argument(
            "--cluuid",
            help="Class UUID",
            type=UUID,
        )
        klass_subparser.add_argument(
            "--name",
            help="Class name",
        )
        klass_subparser.add_argument(
            "--year",
            help="Scolar year",
            default=0,
            type=int,
        )
        klass_subparser.add_argument(
            "--extra",
            help="Extra info",
            choices=["OS", "DF"],
        )

    return parser
