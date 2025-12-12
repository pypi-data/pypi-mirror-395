from typing import Any, Dict, List, Optional, Type, Union

from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_records_resources.services.base.links import (
    EndpointLink,
    Link,
    LinksTemplate,
)

class CommunityLinksTemplate(LinksTemplate):
    def __init__(
        self,
        links: Dict[str, Union[CommunityEndpointLink, CommunityUIEndpointLink]],
        action_link: CommunityEndpointLink,
        available_actions: List[Dict[str, str]],
        context: Optional[Dict[str, Type[CommunityPermissionPolicy]]] = None,
    ) -> None: ...
    def expand(self, identity: Any, obj: Any) -> Dict[str, str]: ...

class CommunityEndpointLink(EndpointLink):
    @staticmethod
    def vars(obj: Any, vars: Dict[str, Any]) -> None: ...

class CommunityUIEndpointLink(EndpointLink):
    @staticmethod
    def vars(obj: Any, vars: Dict[str, Any]) -> None: ...

class CommunityLink(Link):
    @staticmethod
    def vars(obj: Any, vars: Dict[str, Any]) -> None: ...
