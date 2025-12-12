from typing import Any, Dict, Generic, List, Optional, TypeVar

from flask_principal import Identity
from invenio_cache.decorators import cached_with_expiration
from invenio_communities.communities.records.systemfields.deletion_status import (
    CommunityDeletionStatusEnum as CommunityDeletionStatusEnum,
)
from invenio_communities.communities.services.config import CommunityServiceConfig
from invenio_communities.communities.services.links import CommunityLinksTemplate
from invenio_communities.communities.services.results import (
    CommunityFeaturedList,
    CommunityItem,
    CommunityListResult,
)
from invenio_communities.communities.services.uow import (
    CommunityFeaturedCommitOp as CommunityFeaturedCommitOp,
)
from invenio_communities.communities.services.uow import (
    CommunityFeaturedDeleteOp as CommunityFeaturedDeleteOp,
)
from invenio_communities.errors import CommunityDeletedError as CommunityDeletedError
from invenio_communities.errors import (
    CommunityFeaturedEntryDoesNotExistError as CommunityFeaturedEntryDoesNotExistError,
)
from invenio_communities.errors import DeletionStatusError as DeletionStatusError
from invenio_communities.errors import LogoNotFoundError as LogoNotFoundError
from invenio_communities.errors import LogoSizeLimitError as LogoSizeLimitError
from invenio_communities.errors import (
    OpenRequestsForCommunityDeletionError as OpenRequestsForCommunityDeletionError,
)
from invenio_communities.generators import CommunityMembers as CommunityMembers
from invenio_communities.members.services.service import MemberService
from invenio_db.uow import UnitOfWork, dummy_uow
from invenio_records_resources.services.files.results import FileItem
from invenio_records_resources.services.files.service import FileService
from invenio_records_resources.services.records import RecordService
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from invenio_requests.services.requests.results import RequestList
from invenio_requests.services.results import EntityResolverExpandableField
from werkzeug.wsgi import LimitedStream

@cached_with_expiration
def get_cached_community_slug(
    community_id: str, community_service_id: str = "communities"
) -> str: ...

C = TypeVar("C", bound=CommunityServiceConfig)

class CommunityService(RecordService[C], Generic[C]):
    def __init__(
        self,
        config: Any,
        files_service: Optional[FileService] = None,
        invitations_service: Any = None,
        members_service: Optional[MemberService] = None,
    ) -> None: ...
    @property
    def links_item_tpl(self) -> CommunityLinksTemplate: ...
    @property
    def files(self) -> FileService: ...
    @property
    def invitations(self) -> Any: ...
    @property
    def members(self) -> MemberService: ...
    @property
    def schema_featured(self) -> ServiceSchemaWrapper: ...
    @property
    def schema_tombstone(self) -> ServiceSchemaWrapper: ...
    @property
    def expandable_fields(self) -> List[EntityResolverExpandableField]: ...
    def search_user_communities(
        self,
        identity: Identity,
        params: Optional[Dict[str, Any]] = None,
        search_preference: Optional[str] = None,
        extra_filter: Any = None,
        **kwargs: Any,
    ) -> CommunityListResult: ...
    def search_community_requests(
        self,
        identity: Identity,
        community_id: str,
        params: Optional[Dict[str, Any]] = None,
        search_preference: Optional[str] = None,
        expand: bool = False,
        **kwargs: Any,
    ) -> RequestList: ...
    def rename(
        self,
        identity: Identity,
        id_: str,
        data: Dict[str, Any],
        revision_id: Any = None,
        raise_errors: bool = True,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def read_logo(self, identity: Identity, id_: str) -> FileItem: ...
    def update_logo(
        self,
        identity: Identity,
        id_: str,
        stream: LimitedStream,
        content_length: Optional[int] = None,
        uow: UnitOfWork = dummy_uow,
    ) -> FileItem: ...
    def delete_logo(
        self, identity: Identity, id_: str, uow: UnitOfWork = dummy_uow
    ) -> FileItem: ...
    def featured_search(
        self,
        identity: Identity,
        params: Optional[Dict[str, Any]] = None,
        search_preference: Optional[str] = None,
        **kwargs: Any,
    ) -> CommunityListResult: ...
    def featured_list(
        self, identity: Identity, community_id: str
    ) -> CommunityFeaturedList: ...
    def featured_create(
        self,
        identity: Identity,
        community_id: str,
        data: Dict[str, Any],
        raise_errors: bool = True,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def featured_update(
        self,
        identity: Identity,
        community_id: str,
        data: Dict[str, Any],
        featured_id: int,
        raise_errors: bool = True,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def featured_delete(
        self,
        identity: Identity,
        community_id: str,
        featured_id: int,
        raise_errors: bool = True,
        uow: UnitOfWork = dummy_uow,
    ) -> None: ...
    def delete_community(
        self,
        identity: Identity,
        id_: str,
        data: Optional[Dict[str, Any]] = None,
        revision_id: Any = None,
        expand: bool = False,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def delete(
        self,
        identity: Identity,
        id_: str,
        revision_id: Any = ...,
        uow: Optional[UnitOfWork] = ...,
    ) -> Any: ...
    def update_tombstone(
        self,
        identity: Identity,
        id_: str,
        data: Dict[str, Any],
        expand: bool = False,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def restore_community(
        self,
        identity: Identity,
        id_: str,
        expand: bool = False,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def mark_community_for_purge(
        self,
        identity: Identity,
        id_: str,
        expand: bool = False,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def unmark_community_for_purge(
        self,
        identity: Identity,
        id_: str,
        expand: bool = False,
        uow: UnitOfWork = dummy_uow,
    ) -> CommunityItem: ...
    def purge_community(
        self, identity: Identity, id_: str, uow: UnitOfWork = dummy_uow
    ) -> None: ...
    def search(
        self,
        identity: Identity,
        params: Optional[Dict[str, Any]] = None,
        search_preference: Optional[str] = None,
        expand: bool = False,
        extra_filter: Any = None,
        **kwargs: Any,
    ) -> CommunityListResult: ...
    def read(
        self,
        identity: Identity,
        id_: Optional[str],
        expand: bool = False,
        action: str = ...,
    ) -> Any: ...
    def update(
        self,
        identity: Identity,
        id_: str,
        data: Dict[str, Any],
        revision_id: Any = None,
        uow: UnitOfWork = dummy_uow,
        expand: bool = False,
    ) -> CommunityItem: ...
    def on_relation_update(
        self,
        identity: Identity,
        record_type: str,
        records_info: List[Any],
        notif_time: str,
        limit: int = ...,
    ) -> Any: ...
    def bulk_update_parent(
        self,
        identity: Identity,
        community_ids: List[str],
        parent_id: str,
        uow: UnitOfWork = dummy_uow,
    ) -> None: ...
    def search_subcommunities(
        self,
        identity: Identity,
        id_: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> CommunityListResult: ...
