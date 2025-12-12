from typing import Optional, Type

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_requests.customizations.event_types import EventType as EventType
from invenio_requests.customizations.event_types import LogEventType as LogEventType
from invenio_requests.errors import NoSuchActionError as NoSuchActionError
from invenio_requests.proxies import current_events_service as current_events_service
from invenio_requests.records.api import Request

class RequestAction:
    status_from: Optional[tuple[str, ...]]
    status_to: str
    event_type: Optional[Type[EventType]]
    log_event: bool
    request: Request
    def __init__(self, request: Request) -> None: ...
    def can_execute(self) -> bool: ...
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class RequestActions:
    @classmethod
    def can_execute(cls, request: Request, action_name: str) -> bool: ...
    @classmethod
    def get_action(cls, request: Request, action_name: str) -> RequestAction: ...
    @classmethod
    def execute(
        cls, identity: Identity, request: Request, action_name: str, uow: UnitOfWork
    ) -> None: ...

class CreateAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str
    log_event: bool

class CreateAndSubmitAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str
    log_event: bool

class DeleteAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str

class SubmitAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str
    log_event: bool

class AcceptAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str

class DeclineAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str

class CancelAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str

class ExpireAction(RequestAction):
    status_from: Optional[tuple[str, ...]]
    status_to: str
