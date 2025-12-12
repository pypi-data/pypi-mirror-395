from typing import Any

from flask_principal import Identity
from invenio_communities.members.services.service import MemberService
from invenio_communities.notifications.builders import (
    CommunityInvitationAcceptNotificationBuilder as CommunityInvitationAcceptNotificationBuilder,
)
from invenio_communities.notifications.builders import (
    CommunityInvitationCancelNotificationBuilder as CommunityInvitationCancelNotificationBuilder,
)
from invenio_communities.notifications.builders import (
    CommunityInvitationDeclineNotificationBuilder as CommunityInvitationDeclineNotificationBuilder,
)
from invenio_communities.notifications.builders import (
    CommunityInvitationExpireNotificationBuilder as CommunityInvitationExpireNotificationBuilder,
)
from invenio_communities.proxies import current_communities as current_communities
from invenio_db.uow import UnitOfWork
from invenio_requests.customizations import RequestType, actions

def service() -> MemberService: ...

class AcceptAction(actions.AcceptAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class DeclineAction(actions.DeclineAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class CancelAction(actions.CancelAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class ExpireAction(actions.ExpireAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class CommunityInvitation(RequestType):
    type_id: str
    name: str
    create_action: str
    available_actions: dict[str, type]
    creator_can_be_none: bool
    topic_can_be_none: bool
    allowed_creator_ref_types: list[str]
    allowed_receiver_ref_types: list[str]
    allowed_topic_ref_types: list[str]
    needs_context: Any

class CancelMembershipRequestAction(actions.CancelAction):
    def execute(self, identity: Identity, uow: UnitOfWork) -> None: ...

class MembershipRequestRequestType(RequestType):
    type_id: str
    name: str
    create_action: str
    available_actions: dict[str, type]
    creator_can_be_none: bool
    topic_can_be_none: bool
    allowed_creator_ref_types: list[str]
    allowed_receiver_ref_types: list[str]
    allowed_topic_ref_types: list[str]
