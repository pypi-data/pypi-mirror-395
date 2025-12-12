from typing import List

from invenio_communities.communities.records.api import Community as Community
from invenio_communities.proxies import current_communities as current_communities
from invenio_communities.requests.user_moderation.tasks import (
    delete_community as delete_community,
)
from invenio_communities.requests.user_moderation.tasks import (
    restore_community as restore_community,
)

def _get_communities_for_user(user_id: str) -> List[Community]: ...
def on_block(user_id: str, uow=None, **kwargs) -> None: ...
def on_restore(user_id: str, uow=None, **kwargs) -> None: ...
def on_approve(user_id: str, uow=None, **kwargs) -> None: ...
