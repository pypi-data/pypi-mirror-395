from decimal import Decimal
from typing import Optional, Tuple

from _typeshed import Incomplete
from flask_principal import Identity
from invenio_communities.generators import CommunityRoleNeed as CommunityRoleNeed
from invenio_communities.proxies import current_communities as current_communities
from invenio_communities.proxies import (
    current_identities_cache as current_identities_cache,
)
from sqlalchemy.orm.scoping import scoped_session

IDENTITY_KEY: str

def humanize_byte_size(size: int) -> Tuple[Decimal, str]: ...
def identity_cache_key(identity: Identity) -> str: ...
def load_community_needs(identity: Identity) -> None: ...
def on_datastore_post_commit(sender: Incomplete, session: scoped_session) -> None: ...
def on_group_membership_change(community_id: str) -> None: ...
def on_user_membership_change(identity: Optional[Identity] = ...) -> None: ...
