from typing import Any, Callable, Protocol

from invenio_communities.communities.resources.serializer import (
    UICommunityJSONSerializer as UICommunityJSONSerializer,
)
from invenio_communities.proxies import current_communities as current_communities

class _ViewFunc(Protocol):
    def __call__(self, **kwargs: Any) -> Any: ...

def pass_community(serialize: bool) -> Callable[[_ViewFunc], _ViewFunc]: ...
def warn_deprecation(
    deprecated_route: str, new_route: str
) -> Callable[[_ViewFunc], _ViewFunc]: ...
