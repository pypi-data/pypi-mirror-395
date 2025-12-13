import json
import subprocess
from os import environ
import re

from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID
from zipfile import ZipFile


from phystool.config import config
from phystool.helper import as_valid_filename, should_compile
from phystool.latex import (
    PdfLatex,
    LatexLogParser,
    ErrorMessage,
    Latex3Message,
    WarningMessage,
)
from phystool.tags import Tags

if TYPE_CHECKING:
    from phystool.physql.models import PDBRecord


logger = getLogger(__name__)


class PDBFile:
    _ENVIRONMENT: dict[str, str] = dict()
    UUID_PATTERN = re.compile(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
    )

    @classmethod
    def from_record(cls, pdb_record: "PDBRecord") -> "PDBFile":
        """
        Converts a PDBRecord into a  PDBFile
        """
        return PDBFile(
            id=pdb_record.id,
            uuid=pdb_record.uuid,
            pdb_type=pdb_record.pdb_type.name,
            standalone=pdb_record.pdb_type.standalone,
            title=pdb_record.title,
            tags=pdb_record.tags,
            references=sorted([using.uuid for using in pdb_record.using_set]),
        )

    @classmethod
    def from_file(cls, key: UUID | Path) -> "PDBFile":
        """
        Loops over all valid pdb_types and checks if the regex matches the '.tex' file.
        When a match is found, it parses the `.tex` file to extract the PDB_TYPE, the
        optional title and all references to other PDBFiles. The tags are read from the
        related `.json` file if it exists.

        :returns: PDBFile
        """
        if isinstance(key, UUID):
            fname = config.db.DB_DIR / str(key)
            uuid = key
        else:
            fname = key
            uuid = UUID(key.stem)

        with fname.with_suffix(".tex").open() as f:
            tex_content = f.read()
            try:
                with fname.with_suffix(".json").open() as jsin:
                    pdb_data = json.load(jsin)
                    tags = Tags(pdb_data["tags"])
                    pdb_type = pdb_data["pdb_type"]
                    pattern, standalone = config.db.PDB_TYPES[pdb_type]
                    match = pattern.search(tex_content)
            except (FileNotFoundError, json.JSONDecodeError):
                tags = Tags({})
                match = None
                pdb_type = ""
                standalone = False

            if match is None:
                logger.debug("Looking for valid pdb_type")
                for pdb_type, (pattern, standalone) in config.db.PDB_TYPES.items():
                    if match := pattern.search(tex_content):
                        break
                if match is None:
                    raise ValueError(f"Unknown pdb_type for '{fname}'")

            if not match.groups() or match[1] is None:
                title = str(uuid)
            else:
                title = match[1][:50]

            return PDBFile(
                id=0,
                uuid=uuid,
                pdb_type=pdb_type,
                standalone=standalone,
                title=title,
                tags=tags,
                references=sorted(
                    {UUID(uuid[0]) for uuid in cls.UUID_PATTERN.finditer(tex_content)}
                ),
            )

    def __init__(
        self,
        id: int,
        uuid: UUID,
        pdb_type: str,
        standalone: bool,
        title: str,
        tags: Tags,
        references: list[UUID],
    ):
        self.id = id
        self.uuid = uuid
        self.pdb_type = pdb_type
        self.standalone = standalone
        self.title = title
        self.tags = tags
        self.references = references
        self.tex_file = (config.db.DB_DIR / str(self.uuid)).with_suffix(".tex")

    def __repr__(self) -> str:
        return f"PDBFile({self.uuid}:{self.title})"

    def __str__(self) -> str:
        return "{:<3} | {:<50} | {:<20} | {}".format(
            self.pdb_type.upper()[:3], self.title, str(self.uuid), self.tags
        )

    def __lt__(self, other: "PDBFile") -> bool:
        return self.tex_file.stat().st_mtime < other.tex_file.stat().st_mtime

    def save(self) -> None:
        """Saves the .json file"""
        with self.tex_file.with_suffix(".json").open("w") as jsout:
            json.dump(
                {
                    "pdb_type": self.pdb_type,
                    "title": self.title,
                    "tags": self.tags.data,
                    "references": [str(ref) for ref in self.references],
                },
                jsout,
                indent=4,
                ensure_ascii=False,
            )

    def create_tmp_tex_file(self) -> Path:
        if self.standalone:
            return self.tex_file
        tmp_tex_file = Path(f"/tmp/physauto-{self.uuid}.tex")
        with tmp_tex_file.open("w") as out:
            out.write(config.db.template(self.uuid))
        return tmp_tex_file

    def _get_env(self) -> dict[str, str]:
        if not self.__class__._ENVIRONMENT:
            self.__class__._ENVIRONMENT = dict(environ)
            self.__class__._ENVIRONMENT["TEXINPUTS"] = f":{config.db.PHYSTEX}:"
        return self.__class__._ENVIRONMENT

    def compile(self, verbose: bool) -> bool:
        if not should_compile(self.tex_file):
            if verbose:
                logger.debug(f"No compilation required for {self!r}")
            return True

        tmp_tex_file = self.create_tmp_tex_file()
        pdflatex = PdfLatex(tmp_tex_file)
        try:
            pdflatex.compile(env=self._get_env())
            pdflatex.move_pdf(self.tex_file.with_suffix(".pdf"))

            if verbose:
                llp = LatexLogParser(tmp_tex_file, [WarningMessage])
                llp.process()
                llp.as_log()
            return True
        except PdfLatex.CompilationError:
            llp = LatexLogParser(tmp_tex_file, [Latex3Message, ErrorMessage])
            llp.process()
            llp.as_log()
        except PdfLatex.MoveError as e:
            logger.error(e)
        return False

    def zip(self) -> None:
        """
        Create a '.zip' file containing the '.tex' and '.pdf' files of the current
        PDBFile and its references
        """
        fname = as_valid_filename(f"{self.title}") + ".zip"
        with ZipFile(Path.cwd() / fname, "w") as zf:
            self.compile(True)

            files = [config.db.DB_DIR / str(ref) for ref in self.references]
            files.append(self.tex_file)
            for f in set(files):
                zf.write(f.with_suffix(".tex"), arcname=f.with_suffix(".tex").name)
                if f.with_suffix(".pdf").exists():
                    zf.write(f.with_suffix(".pdf"), arcname=f.with_suffix(".pdf").name)

    def bat(self) -> None:
        """Display file in terminal with bat."""
        subprocess.run(
            [
                "bat",
                "--language",
                "tex",
                "--file-name",
                self.title,
                self.tex_file,
            ]
        )
