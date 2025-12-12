from typing import Dict

from invenio_communities.communities.records.api import Community as Community
from invenio_communities.communities.schema import (
    CommunityGhostSchema as CommunityGhostSchema,
)
from invenio_communities.communities.services.config import (
    CommunityServiceConfig as CommunityServiceConfig,
)
from invenio_communities.generators import CommunityRoleNeed as CommunityRoleNeed
from invenio_communities.proxies import (
    current_communities as current_communities,
)
from invenio_communities.proxies import (
    current_roles as current_roles,
)
from invenio_records_resources.references.entity_resolvers import (
    RecordPKProxy,
    RecordResolver,
)

def pick_fields(identity, community_dict): ...

class CommunityPKProxy(RecordPKProxy):
    def ghost_record(self, value): ...
    def get_needs(self, ctx=None): ...
    def pick_resolved_fields(self, identity, resolved_dict): ...

class CommunityResolver(RecordResolver):
    type_id: str
    def __init__(self) -> None: ...
    def _reference_entity(self, entity) -> Dict[str, str]: ...
