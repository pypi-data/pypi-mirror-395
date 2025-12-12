from typing import Any, Dict, Iterator, Optional, Union

from invenio_records.api import Record
from invenio_records.systemfields.relations.modelrelations import ModelRelationResult
from invenio_records.systemfields.relations.relations import RelationBase
from invenio_records.systemfields.relations.results import (
    RelationListResult,
    RelationNestedListResult,
    RelationResult,
)

class RelationsMapping:
    _record: Record
    _fields: Dict[str, RelationBase]
    _cache: Dict[str, Any]

    def __init__(self, record: Record, fields: Dict[str, RelationBase]) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __getattr__(self, name: str) -> Union[
        RelationNestedListResult,
        RelationListResult,
        RelationResult,
        ModelRelationResult,
    ]: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __contains__(self, name: str) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def clean(self, fields: Optional[list[str]] = ...) -> None: ...
    def dereference(self, fields: Optional[list[str]] = ...) -> None: ...
    def validate(self, fields: Optional[list[str]] = ...) -> None: ...
