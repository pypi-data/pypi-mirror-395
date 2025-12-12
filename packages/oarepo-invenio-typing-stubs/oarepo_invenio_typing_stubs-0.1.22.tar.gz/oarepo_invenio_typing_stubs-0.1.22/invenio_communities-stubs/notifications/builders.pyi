from typing import Any, List

from invenio_communities.notifications.generators import (
    CommunityMembersRecipient as CommunityMembersRecipient,
)
from invenio_notifications.models import Notification
from invenio_notifications.services.builders import NotificationBuilder
from invenio_notifications.services.generators import EntityResolve

class BaseNotificationBuilder(NotificationBuilder):
    context: List[EntityResolve]
    recipient_filters: List[Any]  # List of filter objects
    recipient_backends: List[Any]  # List of backend objects

class CommunityInvitationNotificationBuilder(BaseNotificationBuilder): ...

class CommunityInvitationSubmittedNotificationBuilder(
    CommunityInvitationNotificationBuilder
):
    type: str
    @classmethod
    def build(cls, **kwargs: Any) -> Notification: ...  # request, role, message
    recipients: List[Any]  # List of UserRecipient objects

class CommunityInvitationAcceptNotificationBuilder(
    CommunityInvitationNotificationBuilder
):
    type: str
    @classmethod
    def build(cls, **kwargs: Any) -> Notification: ...  # request
    recipients: List[CommunityMembersRecipient]

class CommunityInvitationCancelNotificationBuilder(
    CommunityInvitationNotificationBuilder
):
    type: str
    @classmethod
    def build(cls, **kwargs: Any) -> Notification: ...  # request
    recipients: List[Any]  # List of UserRecipient objects

class CommunityInvitationDeclineNotificationBuilder(
    CommunityInvitationNotificationBuilder
):
    type: str
    @classmethod
    def build(cls, **kwargs: Any) -> Notification: ...  # request
    recipients: List[CommunityMembersRecipient]

class CommunityInvitationExpireNotificationBuilder(
    CommunityInvitationNotificationBuilder
):
    type: str
    @classmethod
    def build(cls, **kwargs: Any) -> Notification: ...  # request
    recipients: List[Any]  # includes both community members and user recipient

class SubCommunityBuilderBase(BaseNotificationBuilder):
    type: str
    context: List[EntityResolve]
    @classmethod
    def build(cls, **kwargs: Any) -> Notification: ...  # identity, request
    recipients: List[Any]  # List of recipient objects
    recipient_filters: List[Any]  # List of filter objects

class SubCommunityCreate(SubCommunityBuilderBase):
    type: str
    recipient_filters: List[Any]  # List of filter objects

class SubCommunityAccept(SubCommunityBuilderBase):
    type: str

class SubCommunityDecline(SubCommunityBuilderBase):
    type: str

class SubComInvitationBuilderBase(SubCommunityBuilderBase):
    type: str
    context: List[EntityResolve]

class SubComInvitationCreate(SubComInvitationBuilderBase):
    type: str
    context: List[EntityResolve]
    recipients: List[Any]  # List of recipient objects

class SubComInvitationAccept(SubComInvitationBuilderBase):
    type: str
    recipient_filters: List[Any]  # List of filter objects

class SubComInvitationDecline(SubComInvitationBuilderBase):
    type: str
    recipient_filters: List[Any]  # List of filter objects

class SubComInvitationExpire(SubComInvitationBuilderBase):
    type: str
    context: List[EntityResolve]
    recipients: List[Any]  # List of recipient objects

class SubComCommentNotificationBuilderBase(SubCommunityBuilderBase):
    context: List[EntityResolve]
    @classmethod
    def build(cls, **kwargs: Any) -> Notification: ...  # request, request_event
    recipient_filters: List[Any]  # List of filter objects

class SubComReqCommentNotificationBuilder(SubComCommentNotificationBuilderBase):
    type: str

class SubComInvCommentNotificationBuilder(SubComCommentNotificationBuilderBase):
    type: str
