from typing import Any, ClassVar

from invenio_records_resources.records.api import Record as _BaseRecord
from invenio_records_resources.references.entity_resolvers import RecordResolver
from invenio_requests.records.api import Request as Request
from invenio_requests.records.api import RequestEvent as RequestEvent
from invenio_requests.services import (
    RequestEventsServiceConfig as RequestEventsServiceConfig,
)
from invenio_requests.services import RequestsServiceConfig as RequestsServiceConfig

class RequestResolver(RecordResolver):
    type_id: ClassVar[str]
    def __init__(self) -> None: ...
    def _reference_entity(self, entity: _BaseRecord) -> dict[str, Any]: ...

class RequestEventResolver(RecordResolver):
    type_id: ClassVar[str]
    def __init__(self) -> None: ...
    def _reference_entity(self, entity: _BaseRecord) -> dict[str, Any]: ...
