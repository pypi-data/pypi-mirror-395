from typing import Any

from flask_principal import ItemNeed, Need
from invenio_records_resources.records.api import Record
from invenio_records_resources.references.entity_resolvers.base import (
    EntityProxy as EntityProxy,
)
from invenio_records_resources.references.entity_resolvers.base import (
    EntityResolver as EntityResolver,
)
from invenio_records_resources.services.base import Service

class ServiceResultProxy(EntityProxy):
    service: Service
    def __init__(
        self, resolver: EntityResolver, ref_dict: dict[str, Any], service: Service
    ) -> None: ...
    def _resolve(self) -> dict[str, Any]: ...
    def get_needs(self, ctx: Any | None = None) -> list[Need | ItemNeed]: ...
    def pick_resolved_fields(
        self, identity: Any, resolved_dict: dict[str, Any]
    ) -> dict[str, Any]: ...

class ServiceResultResolver(EntityResolver):
    type_key: str
    proxy_cls: type[ServiceResultProxy]
    _item_cls: type[Any] | None
    _record_cls: type[Record] | None

    def __init__(
        self,
        service_id: str,
        type_key: str,
        proxy_cls: type[ServiceResultProxy] = ServiceResultProxy,
        item_cls: type[Any] | None = None,
        record_cls: type[Record] | None = None,
    ) -> None: ...
    @property
    def item_cls(self) -> type[Any]: ...
    @property
    def record_cls(self) -> type[Record]: ...
    def matches_entity(self, entity: Any) -> bool: ...
    def matches_reference_dict(self, ref_dict: dict[str, Any]) -> bool: ...
    def _reference_entity(self, entity: Any) -> dict[str, Any]: ...
    def _get_entity_proxy(self, ref_dict: dict[str, Any]) -> ServiceResultProxy: ...
