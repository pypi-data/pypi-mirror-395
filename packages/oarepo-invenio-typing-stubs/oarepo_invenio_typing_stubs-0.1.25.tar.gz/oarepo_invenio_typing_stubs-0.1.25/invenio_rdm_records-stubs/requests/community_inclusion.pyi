from typing import TYPE_CHECKING

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_rdm_records.records.api import RDMDraft, RDMRecord
from invenio_requests.customizations import RequestType, actions

if TYPE_CHECKING:
    # Use TYPE_CHECKING to avoid runtime imports for typing-only dependencies
    from invenio_communities.communities.records.api import Community

def is_access_restriction_valid(
    record: RDMDraft | RDMRecord, community: "Community"
) -> bool: ...

class SubmitAction(actions.SubmitAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class AcceptAction(actions.AcceptAction):
    def execute(self, identity: Identity, uow: UnitOfWork, **kwargs) -> None: ...

class CommunityInclusion(RequestType): ...

def get_request_type(app) -> type[RequestType] | None: ...
