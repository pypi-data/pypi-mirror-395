from typing import Optional, Protocol

from flask.app import Flask
from invenio_requests import config as config
from invenio_requests.registry import TypeRegistry as TypeRegistry
from invenio_requests.resources import (
    RequestCommentsResource as RequestCommentsResource,
)
from invenio_requests.resources import (
    RequestCommentsResourceConfig as RequestCommentsResourceConfig,
)
from invenio_requests.resources import RequestsResource as RequestsResource
from invenio_requests.resources import RequestsResourceConfig as RequestsResourceConfig
from invenio_requests.services import RequestEventsService as RequestEventsService
from invenio_requests.services import (
    RequestEventsServiceConfig as RequestEventsServiceConfig,
)
from invenio_requests.services import RequestsService as RequestsService
from invenio_requests.services import RequestsServiceConfig as RequestsServiceConfig
from invenio_requests.services import (
    UserModerationRequestService as UserModerationRequestService,
)

class _ServiceConfigs(Protocol):
    requests: RequestsServiceConfig
    request_events: RequestEventsServiceConfig

class InvenioRequests:
    requests_service: Optional[RequestsService]
    requests_resource: Optional[RequestsResource]
    request_comments_service: Optional[RequestEventsService]
    _schema_cache: dict[str, object]
    _events_schema_cache: dict[str, object]
    def __init__(self, app: Optional[Flask] = None) -> None: ...
    def init_app(self, app: Flask) -> None: ...
    def init_config(self, app: Flask) -> None: ...
    def service_configs(self, app: Flask) -> _ServiceConfigs: ...
    request_events_service: Optional[RequestEventsService]
    user_moderation_requests_service: Optional[UserModerationRequestService]
    def init_services(self, app: Flask) -> None: ...
    request_events_resource: Optional[RequestCommentsResource]
    def init_resources(self, app: Flask) -> None: ...
    request_type_registry: Optional[TypeRegistry]
    event_type_registry: Optional[TypeRegistry]
    entity_resolvers_registry: Optional[TypeRegistry]
    def init_registry(self, app: Flask) -> None: ...

def register_entry_point(
    registry: TypeRegistry, ep_name: str, app: Optional[Flask] = None
) -> None: ...
def finalize_app(app: Flask) -> None: ...
def api_finalize_app(app: Flask) -> None: ...
def init(app: Flask) -> None: ...
