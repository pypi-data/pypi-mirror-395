from typing import Any, Set

from flask_principal import Identity
from invenio_db.uow import UnitOfWork

class CommunityInclusionService:
    @property
    def supported_types(self) -> Set[str]: ...
    def submit(
        self,
        identity: Identity,
        record: Any,
        community: Any,
        request: Any,
        data: dict[str, Any],
        uow: UnitOfWork,
    ): ...
    def include(
        self, identity: Identity, community: Any, request: Any, uow: UnitOfWork
    ): ...
