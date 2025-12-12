from typing import Any, Dict, Generic, List, Tuple, TypeVar

from _typeshed import Incomplete
from invenio_communities.communities.resources.config import (
    CommunityResourceConfig,
)
from invenio_communities.communities.services.service import CommunityService
from invenio_communities.proxies import current_communities as current_communities
from invenio_records_resources.resources.records.resource import (
    RecordResource,
    request_data,
    request_extra_args,
    request_headers,
    request_search_args,
    request_view_args,
)

request_stream: Incomplete

request_community_requests_search_args: Any

C = TypeVar("C", bound=CommunityResourceConfig)
S = TypeVar("S", bound=CommunityService)

class CommunityResource(RecordResource[C, S], Generic[C, S]):
    def create_url_rules(self) -> List[Dict[str, Any]]: ...
    @request_search_args
    def search_user_communities(self) -> Tuple[Dict[str, Any], int]: ...
    @request_extra_args
    @request_view_args
    @request_community_requests_search_args
    def search_community_requests(self) -> Tuple[Dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def rename(self) -> Tuple[Dict[str, Any], int]: ...
    @request_view_args
    def read_logo(self) -> Any: ...
    @request_view_args
    @request_stream
    def update_logo(self) -> Tuple[Dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def delete(self) -> Any: ...
    @request_headers
    @request_view_args
    @request_data
    def restore_community(self) -> Tuple[Dict[str, Any], int]: ...
    @request_view_args
    def delete_logo(self) -> Any: ...
    @request_search_args
    def featured_communities_search(self) -> Tuple[Dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    def featured_list(self) -> Tuple[Dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def featured_create(self) -> Tuple[Dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def featured_update(self) -> Tuple[Dict[str, Any], int]: ...
    @request_view_args
    def featured_delete(self) -> Any: ...
    @request_view_args
    @request_extra_args
    @request_search_args
    def search_subcommunities(self) -> Tuple[Dict[str, Any], int]: ...
