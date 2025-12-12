from typing import Mapping

from invenio_communities.errors import DeletionStatusError as DeletionStatusError
from invenio_communities.proxies import current_communities as current_communities

def delete_community(
    community_id: str, tombstone_data: Mapping[str, object]
) -> None: ...
def restore_community(community_id: str) -> None: ...
