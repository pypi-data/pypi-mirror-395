from typing import Any, Callable, Optional

from invenio_records.systemfields import SystemField
from invenio_records_resources.records.api import Record
from invenio_records_resources.references.entity_resolvers import EntityProxy

class ReferencedEntityField(SystemField):
    _ref_check: Optional[Callable[[Record, Optional[dict[str, str]]], bool]]
    _registry: Any

    def __init__(
        self,
        key: Optional[str] = ...,
        reference_check_func: Optional[
            Callable[[Record, Optional[dict[str, str]]], bool]
        ] = ...,
        resolver_registry: Any = ...,
    ) -> None: ...
    def _check_reference(
        self, instance: Record, ref_dict: Optional[dict[str, str]]
    ) -> bool: ...
    def set_obj(
        self,
        instance: Record,
        obj: Optional[dict[str, str] | EntityProxy | Any],
    ) -> None: ...
    def obj(self, instance: Record) -> Optional[EntityProxy]: ...

class MultiReferenceEntityField(ReferencedEntityField):
    def set_obj(self, instance: Record, obj: Any) -> None: ...
    def obj(self, instance: Record) -> list[EntityProxy]: ...  # type: ignore[override]

def check_allowed_references(
    get_allows_none: Callable[[Record], bool],
    get_allowed_types: Callable[[Record], list[str]],
    request: Record,
    ref_dict: Optional[dict[str, str]],
) -> bool: ...
