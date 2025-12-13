import datetime
import json

import re
from typing import TypedDict
from uuid import UUID, uuid4
from pathlib import Path
from logging import getLogger

from phystool.config import config
from phystool.pdbfile import PDBFile
from phystool.physql.metadata import filter_pdb_files_by_uuids

logger = getLogger(__name__)


class DataType(TypedDict):
    title: str
    cluuid: UUID
    date: datetime.date
    exercises: list[UUID]


class Klass:
    all: dict[UUID, "Klass"] = dict()

    def __init__(
        self,
        name: str,
        extra: str,
        year: int,
        evaluations: list[UUID] | None = None,
    ):
        self.name = name
        self.year = year or config.CURRENT_SCOLAR_YEAR
        self.extra = extra
        self.evaluations = evaluations or []

    def __lt__(self, other) -> bool:
        return self.year < other.year and self.name < other.name

    def __repr__(self) -> str:
        return f"Klass({self.name} [{self.year}/{self.extra}])"

    def __str__(self) -> str:
        return f"{self.name:<6} [{self.year}/{self.extra}]"

    def is_current(self) -> bool:
        return self.year == config.CURRENT_SCOLAR_YEAR

    def to_dict(self) -> dict[str, str | list[str] | int]:
        return {
            "name": self.name,
            "year": self.year,
            "extra": self.extra,
            "evaluations": [str(ev) for ev in self.evaluations],
        }

    @classmethod
    def search(cls, name: str = "", year: int = 0) -> list[UUID]:
        return [
            uuid
            for uuid, klass in cls.all.items()
            if (
                (name == klass.name if name else True)
                and (year == klass.year if year else True)
            )
        ]

    @classmethod
    def display(cls, uuid: UUID) -> None:
        klass = cls.all[uuid]
        print(f"{klass}")
        for ev_uuid in klass.evaluations:
            print(f"{ev_uuid}: {Evaluation.all[ev_uuid]}")

    @classmethod
    def update(
        cls, uuid: UUID, name: str = "", extra: str = "", year: int = 0
    ) -> "Klass | None":
        if klass := cls.all.get(uuid, None):
            name = name or klass.name
            if year:
                for ev in klass.evaluations:
                    if Evaluation.all[ev].scolar_year != year:
                        logger.error(
                            f"Can't update class having evaluation on year {Evaluation.all[ev].scolar_year}"
                        )
                        return
            else:
                year = klass.year

            if cls.search(name=name, year=year):
                logger.error(
                    f"Can't update class due to conflict on {name=} and {year=}"
                )
                return
            klass = Klass(name=name, extra=extra, year=year)
            cls.all[uuid] = klass
            save()
            return klass
        else:
            logger.error("Can't update a non-existing class")
            return None

    @classmethod
    def create(cls, name: str, extra: str, year: int) -> "Klass | None":
        if not name or not year:
            logger.error(f"Can't create a class with {name=} and {year=}")
            return None
        if cls.search(name=name, year=year):
            logger.error(f"Class with {name=} and {year=} already exists")
            return None
        klass = Klass(name=name, extra=extra, year=year)
        cls.all[uuid4()] = klass
        save()
        return klass


class Evaluation:
    all: dict[UUID, "Evaluation"] = dict()

    def __init__(
        self,
        cluuid: UUID,
        title: str,
        date: datetime.date,
        extra: list[str] | None = None,
        exercises: list[UUID] | None = None,
    ):
        self.cluuid = cluuid
        self.title = title
        self.date = date
        self.extra = extra or []
        self.exercises = exercises or []

    def __lt__(self, other) -> bool:
        return self.date < other.date

    def __repr__(self) -> str:
        out = f"{self.date:%d %b %Y} {self.title:<30} "
        if self.extra:
            out += ",".join(self.extra)
        out += f" ({Klass.all[self.cluuid]})"
        return out

    @property
    def scolar_year(self) -> int:
        return self.date.year if self.date.month > 7 else self.date.year - 1

    def to_dict(self) -> dict[str, str | list[str]]:
        return {
            "cluuid": str(self.cluuid),
            "title": self.title,
            "date": self.date.isoformat(),
            "extra": self.extra,
            "exercises": [str(exo) for exo in self.exercises],
        }

    @classmethod
    def _parse_tex_file(cls, fname: Path) -> DataType:
        with fname.open() as f:
            tex_content = f.read()

        if match := re.search(r"classname=([^,]*)", tex_content):
            name = match.group(1)
        else:
            raise ValueError("Can't match class name")

        if match := re.search(r"title=([^,]*)", tex_content):
            title = match.group(1)
        else:
            raise ValueError("Can't match title")

        if match := re.search(r"date=([^,]*)", tex_content):
            day, month, year_str = match.group(1).split(".")
            year = int(year_str)
            if year < 2000:
                year += 2000
            date = datetime.date(day=int(day), month=int(month), year=year)
            year = date.year if date.month > 7 else date.year - 1
            cluuids = Klass.search(name=name, year=year)
            if len(cluuids) != 1:
                raise ValueError(f"Can't find class {name} in {date.year}")
        else:
            raise ValueError("Can't match title")

        return {
            "title": title,
            "cluuid": cluuids[0],
            "date": date,
            "exercises": [
                UUID(uuid.group(0))
                for uuid in PDBFile.UUID_PATTERN.finditer(tex_content)
            ],
        }

    @classmethod
    def update(cls, evuuid: UUID, fname: Path | None) -> "Evaluation | None":
        if fname is None or fname.suffix != ".tex":
            logger.error("No tex file given")
            return None
        try:
            evaluation = Evaluation(**cls._parse_tex_file(fname))
            Klass.all[Evaluation.all[evuuid].cluuid].evaluations.remove(evuuid)
            Klass.all[evaluation.cluuid].evaluations.append(evuuid)
            Evaluation.all[evuuid] = evaluation
            save()
            return evaluation
        except ValueError as e:
            logger.error(e)
            return None

    @classmethod
    def create(cls, fname: Path | None) -> "Evaluation | None":
        if fname is None or fname.suffix != ".tex":
            logger.error("No tex file given")
            return None
        try:
            evaluation = Evaluation(**cls._parse_tex_file(fname))
            evuuid = uuid4()
            Klass.all[evaluation.cluuid].evaluations.append(evuuid)
            Evaluation.all[evuuid] = evaluation
            save()
            return evaluation
        except ValueError as e:
            logger.error(e)
            return None

    @classmethod
    def display(cls, uuid: UUID) -> None:
        if evaluation := cls.all.get(uuid, None):
            print(f"{evaluation}")
            for pdb_file in filter_pdb_files_by_uuids(evaluation.exercises):
                print(pdb_file)
        else:
            logger.warning(f"Evaluation with {uuid=} not found")

    @classmethod
    def search(
        cls,
        year: int = 0,
        evuuid: UUID | None = None,
        exuuid: UUID | None = None,
        cluuid: UUID | None = None,
    ) -> list[UUID]:
        return [
            uuid
            for uuid, evaluation in cls.all.items()
            if (
                (evuuid == uuid if evuuid else True)
                and (exuuid in evaluation.exercises if exuuid else True)
                and (cluuid == evaluation.cluuid if cluuid else True)
                and (year == evaluation.scolar_year if year else True)
            )
        ]


def save():
    with config.EVALUATION_PATH.open("w") as jsout:
        data = {
            "klasses": {
                str(uuid): klass.to_dict()
                for uuid, klass in sorted(Klass.all.items(), key=lambda x: x[1])
            },
            "evaluations": {
                str(uuid): evaluation.to_dict()
                for uuid, evaluation in sorted(
                    Evaluation.all.items(), key=lambda x: x[1]
                )
            },
        }
        json.dump(data, jsout, indent=4, ensure_ascii=False)


def load_klass_and_evaluation_data() -> None:
    if not config.EVALUATION_PATH.exists():
        raise ValueError
    with config.EVALUATION_PATH.open() as jsin:
        data = json.load(jsin)
        Evaluation.all = {
            UUID(uuid): Evaluation(
                cluuid=UUID(d["cluuid"]),
                title=d["title"],
                date=datetime.datetime.fromisoformat(d["date"]).date(),
                extra=d["extra"],
                exercises=[UUID(ex) for ex in d["exercises"]],
            )
            for uuid, d in data["evaluations"].items()
        }
        Klass.all = {
            UUID(uuid): Klass(
                name=d["name"],
                extra=d["extra"],
                year=d["year"],
                evaluations=[UUID(ev) for ev in d["evaluations"]],
            )
            for uuid, d in data["klasses"].items()
        }
