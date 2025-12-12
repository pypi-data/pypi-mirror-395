from typing import Any, Dict

import marshmallow as ma
from invenio_indexer.api import RecordIndexer
from invenio_records_permissions.policies import BasePermissionPolicy
from invenio_records_resources.services import (
    Link,
    RecordServiceConfig,
    SearchOptions,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_records_resources.services.records.results import RecordItem, RecordList
from invenio_requests.records.api import Request as Request
from invenio_requests.records.api import RequestEvent as RequestEvent

class RequestEventItem(RecordItem):
    @property
    def id(self) -> str: ...

class RequestEventList(RecordList): ...

class RequestEventLink(Link):
    @staticmethod
    def vars(record: RequestEvent, vars: Dict[str, Any]) -> None: ...

class RequestEventsServiceConfig(
    RecordServiceConfig[
        RequestEvent,
        SearchOptions,
        ma.Schema,
        RecordIndexer,
        BasePermissionPolicy,
    ],
    ConfiguratorMixin,
): ...
