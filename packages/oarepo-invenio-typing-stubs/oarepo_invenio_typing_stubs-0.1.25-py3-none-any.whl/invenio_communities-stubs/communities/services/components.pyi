from typing import Any, Dict, List, Optional, Type

from flask_principal import Identity
from invenio_communities.communities.records.api import Community
from invenio_communities.communities.records.systemfields.access import (
    VisibilityEnum as VisibilityEnum,
)
from invenio_communities.communities.records.systemfields.deletion_status import (
    CommunityDeletionStatusEnum as CommunityDeletionStatusEnum,
)
from invenio_communities.generators import CommunityRoleNeed as CommunityRoleNeed
from invenio_communities.proxies import current_roles as current_roles
from invenio_communities.utils import (
    on_user_membership_change as on_user_membership_change,
)
from invenio_oaiserver.models import OAISet
from invenio_records_resources.services.records.components import ServiceComponent

class PIDComponent(ServiceComponent):
    def set_slug(self, record: Community, slug: str) -> None: ...
    def create(
        self,
        identity: Identity,
        record: Optional[Community] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        record: Optional[Community] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None: ...
    def rename(
        self,
        identity: Identity,
        record: Optional[Community] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None: ...

class CommunityAccessComponent(ServiceComponent):
    def _populate_access_and_validate(
        self,
        identity: Identity,
        data: Dict[str, Any],
        record: Optional[Community],
        **kwargs: Any,
    ) -> None: ...
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...

class OwnershipComponent(ServiceComponent):
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...

class FeaturedCommunityComponent(ServiceComponent):
    def featured_create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...

class OAISetComponent(ServiceComponent):
    def _create_set_description(self, community_title: str) -> str: ...
    def _create_set_from_community(self, record: Community) -> OAISet: ...
    def _create_set_spec(self, community_slug: str) -> str: ...
    def _retrieve_set(self, slug: str) -> Optional[OAISet]: ...
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def delete(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def rename(
        self,
        identity: Identity,
        record: Optional[Community] = None,
        data: Optional[Dict[str, Any]] = None,
        old_slug: Optional[str] = None,
        **kwargs: Any,
    ) -> None: ...

class CustomFieldsComponent(ServiceComponent):
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        errors: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...

class CommunityDeletionComponent(ServiceComponent):
    def delete(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def update_tombstone(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def restore(
        self,
        identity: Identity,
        data: None = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def mark(
        self,
        identity: Identity,
        data: None = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def unmark(
        self,
        identity: Identity,
        data: None = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...

class CommunityThemeComponent(ServiceComponent):
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        errors: Optional[List[Any]] = None,
        **kwargs: Any,
    ) -> None: ...

class CommunityParentComponent(ServiceComponent):
    def _validate_and_get_parent(
        self, parent_data: Optional[Dict[str, Any]], child: Community
    ) -> Optional[Community]: ...
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...

class ChildrenComponent(ServiceComponent):
    def _populate_and_validate(
        self, identity: Identity, data: Dict[str, Any], record: Community, **kwargs: Any
    ) -> None: ...
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional[Community] = None,
        **kwargs: Any,
    ) -> None: ...

DefaultCommunityComponents: List[Type[ServiceComponent]]
