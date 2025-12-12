from typing import (
    Any,
    Dict,
    Optional,
)

from invenio_communities.communities.records.api import Community
from invenio_communities.communities.records.systemfields.deletion_status import (
    CommunityDeletionStatusEnum,
)
from invenio_communities.communities.services.results import CommunityItem

from .utils import humanize_byte_size as humanize_byte_size

class CommunityError(Exception):
    """Base exception for community errors."""

class CommunityDeletedError(CommunityError):
    def __init__(
        self, community: Community, result_item: Optional[CommunityItem] = ...
    ) -> None: ...
    community: Community
    result_item: Optional[CommunityItem]

class CommunityFeaturedEntryDoesNotExistError(CommunityError):
    def __init__(self, query_arguments: Dict[str, Any]) -> None: ...

class DeletionStatusError(CommunityError):
    def __init__(
        self, community: Community, expected_status: CommunityDeletionStatusEnum
    ) -> None: ...
    community: Community
    expected_status: CommunityDeletionStatusEnum

class LogoNotFoundError(CommunityError):
    def __init__(self) -> None: ...

class LogoSizeLimitError(CommunityError):
    def __init__(self, limit: int, file_size: int) -> None: ...

class OpenRequestsForCommunityDeletionError(CommunityError):
    def __init__(self, requests: int) -> None: ...

class SetDefaultCommunityError(CommunityError):
    def __init__(self) -> None: ...
