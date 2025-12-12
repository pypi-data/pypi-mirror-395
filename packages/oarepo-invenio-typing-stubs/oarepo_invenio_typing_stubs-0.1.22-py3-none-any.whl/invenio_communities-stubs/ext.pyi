from typing import Optional

from flask import Flask
from invenio_communities.cache.cache import IdentityCache as IdentityCache
from invenio_communities.communities import (
    CommunityFileServiceConfig as CommunityFileServiceConfig,
)
from invenio_communities.communities import CommunityResource as CommunityResource
from invenio_communities.communities import (
    CommunityResourceConfig as CommunityResourceConfig,
)
from invenio_communities.communities import CommunityService as CommunityService
from invenio_communities.communities import (
    CommunityServiceConfig as CommunityServiceConfig,
)
from invenio_communities.members import MemberResource as MemberResource
from invenio_communities.members import MemberResourceConfig as MemberResourceConfig
from invenio_communities.members import MemberService as MemberService
from invenio_communities.members import MemberServiceConfig as MemberServiceConfig
from invenio_communities.roles import RoleRegistry as RoleRegistry
from invenio_communities.subcommunities import (
    SubCommunityResource as SubCommunityResource,
)
from invenio_communities.subcommunities import (
    SubCommunityResourceConfig as SubCommunityResourceConfig,
)
from invenio_communities.subcommunities import (
    SubCommunityService as SubCommunityService,
)
from invenio_communities.subcommunities import (
    SubCommunityServiceConfig as SubCommunityServiceConfig,
)
from invenio_communities.utils import load_community_needs as load_community_needs
from invenio_communities.utils import (
    on_datastore_post_commit as on_datastore_post_commit,
)

from . import config as config

class InvenioCommunities:
    def __init__(self, app: Optional[Flask] = ...) -> None: ...
    def init_app(self, app: Flask) -> None: ...
    roles_registry: RoleRegistry
    def init_config(self, app: Flask) -> None: ...
    service: CommunityService
    subcommunity_service: SubCommunityService
    def init_services(self, app: Flask) -> None: ...
    communities_resource: CommunityResource
    members_resource: MemberResource
    subcommunities_resource: SubCommunityResource
    def init_resource(self, app: Flask) -> None: ...
    def init_hooks(self, app: Flask) -> None: ...
    def cache_handler(self, app: Flask) -> IdentityCache: ...
    cache: IdentityCache
    def init_cache(self, app: Flask) -> None: ...

def api_finalize_app(app: Flask) -> None: ...
def finalize_app(app: Flask) -> None: ...
def register_menus(app: Flask) -> None: ...
def init(app: Flask) -> None: ...
