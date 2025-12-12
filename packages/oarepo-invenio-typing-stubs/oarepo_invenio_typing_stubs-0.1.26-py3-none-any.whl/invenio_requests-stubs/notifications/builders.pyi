from typing import List

from invenio_notifications.models import Notification
from invenio_notifications.services.builders import NotificationBuilder
from invenio_notifications.services.filters import RecipientFilter
from invenio_notifications.services.generators import (
    ContextGenerator,
    RecipientBackendGenerator,
    RecipientGenerator,
)

class CommentRequestEventCreateNotificationBuilder(NotificationBuilder):
    type: str
    context: List[ContextGenerator]
    recipients: List[RecipientGenerator]
    recipient_filters: List[RecipientFilter]
    recipient_backends: List[RecipientBackendGenerator]

    @classmethod
    def build(cls, **kwargs: object) -> Notification: ...
