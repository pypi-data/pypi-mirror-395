from invenio_requests.ext import InvenioRequests
from invenio_requests.registry import TypeRegistry
from invenio_requests.resources import RequestsResource
from invenio_requests.services import (
    RequestEventsService,
    RequestsService,
    UserModerationRequestService,
)

current_requests: InvenioRequests  # intentionally not using a LocalProxy[InvenioRequests] here as mypy does not understand it
current_request_type_registry: TypeRegistry  # intentionally not using a LocalProxy[TypeRegistry] here as mypy does not understand it
current_event_type_registry: TypeRegistry  # intentionally not using a LocalProxy[TypeRegistry] here as mypy does not understand it
current_requests_service: RequestsService  # intentionally not using a LocalProxy[RequestsService] here as mypy does not understand it
current_events_service: RequestEventsService  # intentionally not using a LocalProxy[RequestEventsService] here as mypy does not understand it
current_requests_resource: RequestsResource  # intentionally not using a LocalProxy[RequestsResource] here as mypy does not understand it
current_user_moderation_service: UserModerationRequestService  # intentionally not using a LocalProxy[UserModerationRequestService] here as mypy does not understand it
