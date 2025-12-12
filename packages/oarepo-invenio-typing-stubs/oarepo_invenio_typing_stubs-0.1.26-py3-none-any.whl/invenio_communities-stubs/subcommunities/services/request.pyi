from typing import Any, Type

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_requests.customizations import RequestType, actions
from invenio_requests.customizations.actions import RequestAction
from werkzeug.wrappers import Response as Flask

# Note: Builders are used only as types; keep them as Any to avoid import issues in stubs
SubComInvCommentNotificationBuilder: type[Any]
SubComReqCommentNotificationBuilder: type[Any]

class AcceptSubcommunity(actions.AcceptAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class DeclineSubcommunity(actions.DeclineAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class SubCommunityRequest(RequestType):
    type_id: str
    name: str
    creator_can_be_none: bool
    topic_can_be_none: bool
    allowed_creator_ref_types: list[str]
    allowed_receiver_ref_types: list[str]
    allowed_topic_ref_types: list[str]
    comment_notification_builder: type[Any]
    available_actions: dict[str, type[RequestAction]]
    needs_context: Any

class CreateSubcommunityInvitation(actions.CreateAndSubmitAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class AcceptSubcommunityInvitation(actions.AcceptAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class DeclineSubcommunityInvitation(actions.DeclineAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class SubCommunityInvitationRequest(RequestType):
    type_id: str
    name: str
    creator_can_be_none: bool
    topic_can_be_none: bool
    allowed_creator_ref_types: list[str]
    allowed_receiver_ref_types: list[str]
    allowed_topic_ref_types: list[str]
    comment_notification_builder: type[Any]
    available_actions: dict[str, type[RequestAction]]
    needs_context: Any

def subcommunity_request_type(app: Flask) -> Type[SubCommunityRequest] | None: ...
def subcommunity_invitation_request_type(
    app: Flask,
) -> Type[SubCommunityInvitationRequest] | None: ...
