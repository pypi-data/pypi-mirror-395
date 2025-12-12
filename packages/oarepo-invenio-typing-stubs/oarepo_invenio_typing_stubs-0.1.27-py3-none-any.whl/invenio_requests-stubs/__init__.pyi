from invenio_requests.customizations import RequestAction as RequestAction
from invenio_requests.ext import InvenioRequests as InvenioRequests
from invenio_requests.proxies import (
    current_event_type_registry as current_event_type_registry,
)
from invenio_requests.proxies import current_events_service as current_events_service
from invenio_requests.proxies import (
    current_request_type_registry as current_request_type_registry,
)
from invenio_requests.proxies import current_requests as current_requests
from invenio_requests.proxies import (
    current_requests_resource as current_requests_resource,
)
from invenio_requests.proxies import (
    current_requests_service as current_requests_service,
)

__all__ = [
    "__version__",
    "current_event_type_registry",
    "current_events_service",
    "current_request_type_registry",
    "current_requests_resource",
    "current_requests_service",
    "current_requests",
    "InvenioRequests",
    "RequestAction",
]

__version__: str
