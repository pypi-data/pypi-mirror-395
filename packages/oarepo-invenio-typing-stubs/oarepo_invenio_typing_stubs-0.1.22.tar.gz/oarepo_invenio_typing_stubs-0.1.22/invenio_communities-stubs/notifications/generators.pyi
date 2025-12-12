from typing import Dict, List, Optional

from invenio_communities.proxies import current_communities as current_communities
from invenio_notifications.models import Notification, Recipient
from invenio_notifications.services.generators import RecipientGenerator

class CommunityMembersRecipient(RecipientGenerator):
    key: str
    roles: Optional[List[str]]
    def __init__(self, key: str, roles: Optional[List[str]] = ...) -> None: ...
    def __call__(
        self, notification: Notification, recipients: dict
    ) -> Dict[str, Recipient]: ...
