from typing import Any, Dict, List, Optional, Type

from invenio_records.api import Record
from invenio_records.systemfields.relations.results import RelationResult

class RelationBase:
    result_cls: Type[RelationResult]
    key: Optional[str]
    attrs: List[str]
    keys: List[str]
    _value_key_suffix: str
    _clear_empty: bool
    _cache_key: Optional[str]
    value_check: Optional[Any]
    _cache_ref: Optional[Dict[str, Any]]

    def __init__(
        self,
        key: Optional[str] = ...,
        attrs: Optional[List[str]] = ...,
        keys: Optional[List[str]] = ...,
        _value_key_suffix: str = ...,
        _clear_empty: bool = ...,
        cache_key: Optional[str] = ...,
        value_check: Optional[Any] = ...,
    ): ...
    def inject_cache(
        self, cache: Dict[str, Dict[Any, Any]], default_key: str
    ) -> None: ...
    @property
    def cache(self) -> Dict[str, Any]: ...
    def resolve(self, id_: str) -> Optional[Record]: ...
    @property
    def value_key(self) -> str: ...
    def exists(self, id_: str) -> bool: ...
    def exists_many(self, ids: Any) -> bool: ...
    def get_value(self, record: Record) -> RelationResult: ...
    def parse_value(self, value: Any) -> Any: ...
    def set_value(self, record: Record, value: Any) -> None: ...
    def clear_value(self, record: Record) -> None: ...

class PKRelation(RelationBase):
    record_cls: Type[Record]

    def __init__(self, *args: Any, record_cls: Type[Record] = ..., **kwargs: Any): ...
    def resolve(self, id_: str) -> Optional[Record]: ...

class ListRelation(RelationBase):
    relation_field: Optional[str]

    def __init__(
        self, *args: Any, relation_field: Optional[str] = ..., **kwargs: Any
    ): ...
    def _get_parent(self, record: Record, keys: List[str]) -> Dict[str, Any]: ...

class PKListRelation(ListRelation, PKRelation):
    """Primary-key list relation."""

class NestedListRelation(ListRelation):
    def exists_many(self, ids: List[List[str]]) -> bool: ...

class PKNestedListRelation(NestedListRelation, PKRelation):
    """Primary-key nested list relation."""
