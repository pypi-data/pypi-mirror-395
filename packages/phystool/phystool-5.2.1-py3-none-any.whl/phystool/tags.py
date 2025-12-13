from logging import getLogger
from locale import strxfrm
from typing import Iterator

logger = getLogger(__name__)


class TagManager:
    def __init__(self) -> None:
        self._tags: Tags | None = None
        self._id_tuple_map: dict[int, tuple[str, str]] = {}
        self._tuple_id_map: dict[str, dict[str, int]] = {}

    @property
    def tags(self) -> "Tags":
        if self._tags is None:
            self.reload_from_db()
            return self.tags
        return self._tags

    def from_ids(self, tag_ids: set[int]) -> "Tags":
        if not self._id_tuple_map:
            self.reload_from_db()

        tmp: dict[str, set[str]] = {}
        for tag_id in tag_ids:
            category_name, tag_name = self._id_tuple_map[tag_id]
            try:
                tmp[category_name].add(tag_name)
            except KeyError:
                tmp[category_name] = {tag_name}
        return Tags(tmp)

    def get_id(self, category_name: str, tag_name: str) -> int:
        try:
            return self._tuple_id_map[category_name][tag_name]
        except KeyError:
            self.reload_from_db()
            return self._tuple_id_map[category_name][tag_name]

    def reload_from_db(self) -> None:
        from sqlalchemy.sql.expression import select

        from phystool.physql import physql_db
        from phystool.physql.models import Tag, Category

        self._id_tuple_map = {}
        self._tuple_id_map = {}
        tmp: dict[str, set[str]] = {}
        with physql_db() as session:
            for tag_id, tag_name, category_name in session.execute(
                select(Tag.id, Tag.name, Category.name)
                .join(Tag, Category.tag_set)
                .order_by(Category.name, Tag.name)
            ):
                self._id_tuple_map[tag_id] = (category_name, tag_name)
                try:
                    tmp[category_name].add(tag_name)
                    self._tuple_id_map[category_name][tag_name] = tag_id
                except KeyError:
                    tmp[category_name] = {tag_name}
                    self._tuple_id_map[category_name] = {tag_name: tag_id}
        self._tags = Tags(tmp)


class Tags:
    """
    Helper class that manages tags.

    :param tags: tags sorted by category
    """

    manager = TagManager()

    def __init__(self, tags: dict[str, set[str]]):
        self.data = {
            category: sorted(tags, key=strxfrm)
            for category, tags in tags.items()
            if tags  # NOTE: category should't be an empty list
        }

    def __iter__(self) -> Iterator[tuple[str, list[str]]]:
        for category, tags in self.data.items():
            yield category, tags

    def __add__(self, other: "Tags") -> "Tags":
        # NOTE: use an empty Tag to avoid redundant sort in __init__
        out = Tags({})
        out.data = self.data.copy()
        out += other
        return out

    def __iadd__(self, other: "Tags") -> "Tags":
        self.data = {
            category: sorted(tags, key=strxfrm)
            for category in sorted(self.data.keys() | other.data.keys())
            if (tags := set(self.data.get(category, []) + other.data.get(category, [])))
        }
        return self

    def __sub__(self, other: "Tags") -> "Tags":
        # NOTE: use an empty Tag to avoid redundant sort in __init__
        out = Tags({})
        out.data = self.data.copy()
        out -= other
        return out

    def __isub__(self, other: "Tags") -> "Tags":
        self.data = {
            category: sorted(tags, key=strxfrm)
            for category in sorted(self.data.keys() | other.data.keys())
            if (
                tags := set(self.data.get(category, []))
                - set(other.data.get(category, []))
            )
        }
        return self

    def __bool__(self) -> bool:
        for tags in self.data.values():
            if tags:
                return True
        return False

    def __str__(self) -> str:
        return ", ".join([tag for tags in self.data.values() for tag in tags])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tags):
            return False

        if len(self.data.keys()) != len(other.data.keys()):
            return False

        for category, tags in self:
            if set(other.data.get(category, [])) != set(tags):
                return False
        return True

    def display(self) -> None:
        for category, tags in self:
            for tag in tags:
                print(self.manager.get_id(category, tag), tag)

    def as_ids(self) -> set[int]:
        return {
            self.manager.get_id(category, tag)
            for category, tags in self.data.items()
            for tag in tags
        }

    def with_overlap(self, other: "Tags") -> bool:
        """
        Returns `False` if a category doesn't share any tag between this instance and
        the other instance, otherwise, returns `True`
        """
        # WARNING: Returns `False` if, for any category, either set or the two sets are
        # empty (should not happen in the code).
        if other:
            for category in other.data.keys():
                if set(self.data.get(category, [])).isdisjoint(
                    other.data.get(category, [])
                ):
                    return False
        return True

    def without_overlap(self, other: "Tags") -> bool:
        """
        Returns `False` if a category shares at least one tag between this instance and
        the other instance, otherwise, returns `True`
        """
        # WARNING: Doesn't necessarily return `True` if, for a given category, either
        # set or the two sets are empty (should not happen in the code).
        if other:
            for category in other.data.keys():
                if not set(self.data.get(category, [])).isdisjoint(
                    other.data.get(category, [])
                ):
                    return False
        return True
