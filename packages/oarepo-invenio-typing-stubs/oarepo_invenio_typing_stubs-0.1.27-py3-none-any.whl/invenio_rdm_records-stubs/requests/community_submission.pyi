from typing import TYPE_CHECKING

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_rdm_records.requests.base import ReviewRequest
from invenio_requests.customizations import actions

if TYPE_CHECKING:
    from flask import Flask

class SubmitAction(actions.SubmitAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class AcceptAction(actions.AcceptAction):
    def execute(self, identity: Identity, uow: UnitOfWork, **kwargs) -> None: ...

class DeclineAction(actions.DeclineAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class CancelAction(actions.CancelAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class ExpireAction(actions.ExpireAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class CommunitySubmission(ReviewRequest): ...

def get_request_type(app: "Flask" | None) -> type[ReviewRequest] | None: ...
