# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any, ClassVar, Optional, overload

from flask_principal import Identity
from invenio_notifications.models import Notification
from invenio_notifications.services.builders import NotificationBuilder
from invenio_notifications.services.filters import RecipientFilter
from invenio_notifications.services.generators import (
    ContextGenerator,
    RecipientBackendGenerator,
    RecipientGenerator,
)
from invenio_records_resources.records.api import Record
from invenio_requests.records.api import Request

class CommunityInclusionNotificationBuilder(NotificationBuilder):
    """Base notification builder for record community inclusion events."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class CommunityInclusionSubmittedNotificationBuilder(
    CommunityInclusionNotificationBuilder,
):
    """Notification builder for record community inclusion submitted."""

    type: ClassVar[str]

class GuestAccessRequestTokenCreateNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, record: Record, email: str, verify_url: str) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class GuestAccessRequestDeclineNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class GuestAccessRequestCancelNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request, identity: Identity) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class GuestAccessRequestSubmittedNotificationBuilder(NotificationBuilder):
    """Notification builder for submitted guest access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class GuestAccessRequestSubmitNotificationBuilder(NotificationBuilder):
    """Notification builder for guest access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class GuestAccessRequestAcceptNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request, access_url: str) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class UserAccessRequestDeclineNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class UserAccessRequestCancelNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request, identity: Identity) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class UserAccessRequestSubmitNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class UserAccessRequestAcceptNotificationBuilder(NotificationBuilder):
    """Notification builder for user access requests."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class GrantUserAccessNotificationBuilder(NotificationBuilder):
    """Notification builder for user access grant."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(
        cls,
        record: Record,
        user: Any,
        permission: str,
        message: Optional[str] = ...,
    ) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class CommunityInclusionActionNotificationBuilder(NotificationBuilder):
    """Notification builder for inclusion actions."""

    type: ClassVar[str]

    @classmethod
    @overload
    def build(cls, identity: Identity, request: Request) -> Notification: ...
    @classmethod
    @overload
    def build(cls, **kwargs) -> Notification: ...

    context: ClassVar[list[ContextGenerator]]
    recipients: ClassVar[list[RecipientGenerator]]
    recipient_filters: ClassVar[list[RecipientFilter]]
    recipient_backends: ClassVar[list[RecipientBackendGenerator]]

class CommunityInclusionAcceptNotificationBuilder(
    CommunityInclusionActionNotificationBuilder,
):
    """Notification builder for inclusion accept action."""

    type: ClassVar[str]

class CommunityInclusionCancelNotificationBuilder(
    CommunityInclusionActionNotificationBuilder,
):
    """Notification builder for inclusion cancel action."""

    type: ClassVar[str]
    recipients: ClassVar[list[RecipientGenerator]]

class CommunityInclusionDeclineNotificationBuilder(
    CommunityInclusionActionNotificationBuilder,
):
    """Notification builder for inclusion decline action."""

    type: ClassVar[str]

class CommunityInclusionExpireNotificationBuilder(
    CommunityInclusionActionNotificationBuilder,
):
    """Notification builder for inclusion expire action."""

    type: ClassVar[str]
    context: ClassVar[list[ContextGenerator]]
