from logging import getLogger
from pathlib import Path
from uuid import UUID

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql.schema import Column, ForeignKey, Table, UniqueConstraint

from phystool.config import config
from phystool.physql import BaseModel
from phystool.tags import Tags


logger = getLogger(__name__)


class Category(BaseModel):
    __tablename__ = "category"
    __table_args__ = (UniqueConstraint("name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    tag_set: Mapped[set["Tag"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name=}, {self.id}>"


tag_relation = Table(
    "tagrelation",
    BaseModel.metadata,
    Column(
        "pdb_record_id",
        ForeignKey("pdb_record.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        ForeignKey("tag.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Tag(BaseModel):
    __tablename__ = "tag"
    __table_args__ = (UniqueConstraint("name", "category_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped[Category] = relationship(back_populates="tag_set")
    pdb_record_set: Mapped[set["PDBRecord"]] = relationship(
        secondary=tag_relation, back_populates="tag_set"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name=}, {self.id}>"


class PDBType(BaseModel):
    __tablename__ = "pdb_type"
    __table_args__ = (UniqueConstraint("name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    standalone: Mapped[bool]
    pdb_record_set: Mapped[set["PDBRecord"]] = relationship(back_populates="pdb_type")


record_to_record = Table(
    "record_to_record",
    BaseModel.metadata,
    Column(
        "using_id",
        ForeignKey("pdb_record.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "used_by_id",
        ForeignKey("pdb_record.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class PDBRecord(BaseModel):
    __tablename__ = "pdb_record"
    __table_args__ = (UniqueConstraint("uuid"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID]
    title: Mapped[str]
    pdb_type_id: Mapped[int] = mapped_column(ForeignKey("pdb_type.id"))
    pdb_type: Mapped[PDBType] = relationship(back_populates="pdb_record_set")
    tag_set: Mapped[set[Tag]] = relationship(
        secondary=tag_relation,
        back_populates="pdb_record_set",
    )
    using_set: Mapped[set["PDBRecord"]] = relationship(
        "PDBRecord",
        secondary=record_to_record,
        primaryjoin=id == record_to_record.c.used_by_id,
        secondaryjoin=id == record_to_record.c.using_id,
        back_populates="used_by_set",
    )
    used_by_set: Mapped[set["PDBRecord"]] = relationship(
        "PDBRecord",
        secondary=record_to_record,
        primaryjoin=id == record_to_record.c.using_id,
        secondaryjoin=id == record_to_record.c.used_by_id,
        back_populates="using_set",
    )

    @property
    def tex_file(self) -> Path:
        return (config.db.DB_DIR / str(self.uuid)).with_suffix(".tex")

    @property
    def tags(self) -> Tags:
        if not hasattr(self, "_tags"):
            self._tags = Tags.manager.from_ids({tag.id for tag in self.tag_set})
        return self._tags
