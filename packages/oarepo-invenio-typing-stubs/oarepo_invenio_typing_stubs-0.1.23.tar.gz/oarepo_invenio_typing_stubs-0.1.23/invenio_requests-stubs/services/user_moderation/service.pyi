from typing import Any, Dict, List, Optional, Type

from flask_principal import Identity
from invenio_db.uow import UnitOfWork, dummy_uow
from invenio_requests.customizations.user_moderation.user_moderation import (
    UserModerationRequest as UserModerationRequest,
)
from invenio_requests.proxies import (
    current_request_type_registry as current_request_type_registry,
)
from invenio_requests.services.requests.results import RequestItem
from invenio_requests.services.requests.service import RequestsService
from invenio_requests.services.results import (
    EntityResolverExpandableField as EntityResolverExpandableField,
)
from invenio_requests.services.user_moderation.errors import (
    OpenRequestAlreadyExists as OpenRequestAlreadyExists,
)

class UserModerationRequestService:
    requests_service: RequestsService
    def __init__(self, requests_service: RequestsService) -> None: ...
    @property
    def request_type_cls(self) -> Type[Any]: ...
    @property
    def expandable_fields(self) -> List[EntityResolverExpandableField]: ...
    def _create_request(
        self,
        identity: Identity,
        user_id: str,
        creator: str,
        receiver: str,
        data: Dict[str, Any],
        uow: UnitOfWork,
    ) -> RequestItem: ...
    def _exists(self, identity: Identity, user_id: str) -> Optional[str]: ...
    def request_moderation(
        self,
        identity: Identity,
        user_id: str,
        data: Optional[Dict[str, Any]] = None,
        uow: UnitOfWork = dummy_uow,
        **kwargs: Any,
    ) -> RequestItem: ...
