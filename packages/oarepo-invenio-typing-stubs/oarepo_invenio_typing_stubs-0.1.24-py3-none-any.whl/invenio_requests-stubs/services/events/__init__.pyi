from invenio_requests.services.events.config import (
    RequestEventsServiceConfig as RequestEventsServiceConfig,
)
from invenio_requests.services.events.service import (
    RequestEventsService as RequestEventsService,
)

__all__ = ["RequestEventsService", "RequestEventsServiceConfig"]
