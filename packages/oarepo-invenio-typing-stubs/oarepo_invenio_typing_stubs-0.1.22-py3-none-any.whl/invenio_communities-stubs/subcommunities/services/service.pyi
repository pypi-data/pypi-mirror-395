from typing import Any, Dict, Generic, Optional, Type, TypeVar

from flask_principal import Identity
from invenio_communities.communities import CommunityService
from invenio_communities.proxies import current_communities as current_communities
from invenio_communities.proxies import current_roles as current_roles
from invenio_communities.subcommunities.services.config import (
    SubCommunityServiceConfig,
)
from invenio_communities.subcommunities.services.request import SubCommunityRequest
from invenio_db.uow import UnitOfWork, dummy_uow
from invenio_records_resources.services.base import Service
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from invenio_requests.services.requests.results import RequestItem

community_service: CommunityService  # intentionally not using a LocalProxy[CommunityService] here as mypy does not understand it (LocalProxy to current_communities.service)

C = TypeVar("C", bound=SubCommunityServiceConfig)

class SubCommunityService(Service[C], Generic[C]):
    def _is_owner_of(self, identity: Identity, community: str) -> Any: ...
    @property
    def request_cls(self) -> Type[SubCommunityRequest]: ...
    @property
    def schema(self) -> ServiceSchemaWrapper: ...
    @property
    def links_item_tpl(self) -> Any: ...
    @property
    def expandable_fields(self) -> Any: ...
    def join(
        self,
        identity: Identity,
        id_: str,
        data: Dict[str, Any],
        uow: Optional[UnitOfWork] = ...,
    ) -> RequestItem: ...
    def create_subcommunity_invitation_request(
        self,
        identity: Identity,
        parent_community_id: str,
        child_community_id: str,
        data: Dict[str, Any],
        expires_at: Optional[Any] = None,
        uow: UnitOfWork = dummy_uow,
    ) -> None: ...
