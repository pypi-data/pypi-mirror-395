from __future__ import annotations

from flask_principal import Identity
from invenio_db.uow import UnitOfWork

class SubmissionCreateAction:
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class SubmissionCancelAction:
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class CommunitySubmission:
    available_actions: dict[str, type]

class InclusionSubmitAction:
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class InclusionCancelAction:
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class CommunityInclusion:
    available_actions: dict[str, type]
