from typing import Any, Dict, Generic, List, Tuple, TypeVar

from flask_resources import Resource, response_handler
from invenio_communities.subcommunities.resources.config import (
    SubCommunityResourceConfig,
)
from invenio_communities.subcommunities.services.service import SubCommunityService
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_view_args,
)

C = TypeVar("C", bound=SubCommunityResourceConfig)
S = TypeVar("S", bound=SubCommunityService)

class SubCommunityResource(Resource[C], Generic[C, S]):
    service: S
    def __init__(self, config: C, service: S) -> None: ...
    def create_url_rules(self) -> List[Dict[str, Any]]: ...
    @request_view_args
    @response_handler()
    @request_data
    def join(self) -> Tuple[Dict[str, Any], int]: ...
