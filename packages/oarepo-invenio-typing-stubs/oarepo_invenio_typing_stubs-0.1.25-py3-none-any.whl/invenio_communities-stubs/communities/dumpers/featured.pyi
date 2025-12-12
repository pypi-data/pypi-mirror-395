from typing import Any, Dict

from invenio_communities.communities.records.models import (
    CommunityFeatured as CommunityFeatured,
)
from invenio_records.dumpers import SearchDumperExt

class FeaturedDumperExt(SearchDumperExt):
    key: str
    def __init__(self, key: str = "featured") -> None: ...
    def dump(self, record: Any, data: Dict[str, Any]) -> None: ...
    def load(self, data: Dict[str, Any], record_cls: type) -> None: ...
