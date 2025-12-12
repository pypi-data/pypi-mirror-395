from typing import Any

from flask_principal import ItemNeed, Need
from invenio_records_resources.records.api import Record
from invenio_records_resources.references.entity_resolvers.base import (
    EntityProxy as EntityProxy,
)
from invenio_records_resources.references.entity_resolvers.base import (
    EntityResolver as EntityResolver,
)

class RecordProxy(EntityProxy):
    record_cls: type[Record]
    def __init__(
        self,
        resolver: EntityResolver,
        ref_dict: dict[str, Any],
        record_cls: type[Record],
    ) -> None: ...
    def _resolve(self) -> Record: ...
    def get_needs(self, ctx: Any = None) -> list[Need | ItemNeed]: ...
    def pick_resolved_fields(
        self, identity: Any, resolved_dict: dict[str, Any]
    ) -> dict[str, Any]: ...

class RecordPKProxy(RecordProxy):
    def _resolve(self) -> Record: ...

class RecordResolver(EntityResolver):
    record_cls: type[Record]
    type_key: str
    proxy_cls: type[RecordProxy]
    def __init__(
        self,
        record_cls: type[Record],
        service_id: str,
        type_key: str = "record",
        proxy_cls: type[RecordProxy] = ...,
    ) -> None: ...
    def matches_entity(self, entity: Any) -> bool: ...
    def _reference_entity(self, entity: Record) -> dict[str, Any]: ...
    def matches_reference_dict(self, ref_dict: dict[str, Any]) -> bool: ...
    def _get_entity_proxy(self, ref_dict: dict[str, Any]) -> RecordProxy: ...
