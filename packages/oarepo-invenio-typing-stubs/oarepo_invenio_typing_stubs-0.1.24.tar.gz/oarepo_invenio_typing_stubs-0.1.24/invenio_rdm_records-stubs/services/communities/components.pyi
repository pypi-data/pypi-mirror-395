from typing import Any

from flask_principal import Identity
from invenio_communities.communities.services.components import (
    ChildrenComponent as ChildrenComponent,
)
from invenio_communities.communities.services.components import (
    CommunityAccessComponent as BaseAccessComponent,
)
from invenio_communities.communities.services.components import (
    CommunityDeletionComponent as CommunityDeletionComponent,
)
from invenio_communities.communities.services.components import (
    CommunityParentComponent as CommunityParentComponent,
)
from invenio_communities.communities.services.components import (
    CommunityThemeComponent as CommunityThemeComponent,
)
from invenio_communities.communities.services.components import (
    CustomFieldsComponent as CustomFieldsComponent,
)
from invenio_communities.communities.services.components import (
    FeaturedCommunityComponent as FeaturedCommunityComponent,
)
from invenio_communities.communities.services.components import (
    OAISetComponent as OAISetComponent,
)
from invenio_communities.communities.services.components import (
    OwnershipComponent as OwnershipComponent,
)
from invenio_communities.communities.services.components import (
    PIDComponent as PIDComponent,
)
from invenio_rdm_records.services.communities.moderation import (
    ContentModerationComponent as ContentModerationComponent,
)
from invenio_records_resources.services.records.components import (
    MetadataComponent as MetadataComponent,
)
from invenio_records_resources.services.records.components import (
    RelationsComponent as RelationsComponent,
)

class CommunityAccessComponent(BaseAccessComponent):
    def _check_visibility(self, identity: Identity, record: Any) -> None: ...
    def update(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: Any | None = ...,
        **kwargs: Any,
    ) -> None: ...

CommunityServiceComponents: list[type]
