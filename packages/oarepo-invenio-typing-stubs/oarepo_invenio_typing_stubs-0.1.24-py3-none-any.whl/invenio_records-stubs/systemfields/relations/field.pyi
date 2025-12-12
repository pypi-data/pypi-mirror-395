from typing import Dict, Iterator, Self, Union, overload

from invenio_records.api import Record
from invenio_records.systemfields.base import SystemField
from invenio_records.systemfields.relations.mapping import RelationsMapping
from invenio_records.systemfields.relations.relations import (
    PKListRelation,
    PKNestedListRelation,
    PKRelation,
    RelationBase,
)

class RelationsField[R: Record = Record](SystemField):  # type: ignore[misc]
    _original_fields: Dict[str, RelationBase]

    def __init__(self, **fields: RelationBase): ...
    def __getattr__(
        self, name: str
    ) -> Union[PKListRelation, PKRelation, PKNestedListRelation]: ...
    def __iter__(self) -> Iterator[RelationBase]: ...
    def __contains__(self, name: str) -> bool: ...
    @property
    def _fields(
        self,
    ) -> Dict[str, RelationBase]: ...
    def obj(self, instance: R) -> RelationsMapping: ...
    def pre_commit(self, record: R) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Record, owner: type[Record]
    ) -> RelationsMapping: ...
    def __set__(self, instance: Record, value: RelationsMapping) -> None: ...  # type: ignore[override]

class MultiRelationsField[R: Record = Record](RelationsField[R]):
    _relation_fields: set[str]

    def __init__(self, **fields: Union[RelationBase, RelationsField]): ...
