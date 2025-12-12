from typing import Any, Dict, Optional

from invenio_notifications.models import Notification, Recipient
from invenio_requests.proxies import current_events_service as current_events_service

class RequestParticipantsRecipient:
    key: str
    def __init__(self, key: str) -> None: ...
    def _get_user_id(self, request_field: Dict[str, Any]) -> Optional[str]: ...
    def __call__(
        self, notification: Notification, recipients: Dict[str, Recipient]
    ) -> Dict[str, Recipient]: ...
