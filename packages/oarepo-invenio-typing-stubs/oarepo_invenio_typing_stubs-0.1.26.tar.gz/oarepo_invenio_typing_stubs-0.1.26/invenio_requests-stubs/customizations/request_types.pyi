from collections.abc import Mapping
from typing import Any, Dict, List, Optional, Type

from flask_babel.speaklater import LazyString
from flask_principal import Need
from invenio_requests.customizations.actions import AcceptAction as AcceptAction
from invenio_requests.customizations.actions import CancelAction as CancelAction
from invenio_requests.customizations.actions import CreateAction as CreateAction
from invenio_requests.customizations.actions import DeclineAction as DeclineAction
from invenio_requests.customizations.actions import DeleteAction as DeleteAction
from invenio_requests.customizations.actions import ExpireAction as ExpireAction
from invenio_requests.customizations.actions import RequestAction
from invenio_requests.customizations.actions import SubmitAction as SubmitAction
from invenio_requests.customizations.states import RequestState
from invenio_requests.notifications.builders import (
    CommentRequestEventCreateNotificationBuilder as CommentRequestEventCreateNotificationBuilder,
)
from invenio_requests.proxies import current_requests as current_requests
from invenio_requests.records.api import Request
from marshmallow import Schema
from marshmallow.fields import Field

class RequestType:
    type_id: str
    name: str | LazyString
    available_statuses: Dict[str, RequestState]
    create_action: str
    delete_action: str
    available_actions: Dict[str, Type[RequestAction]]
    creator_can_be_none: bool
    receiver_can_be_none: bool
    topic_can_be_none: bool
    allowed_creator_ref_types: List[str]
    allowed_receiver_ref_types: List[str]
    allowed_topic_ref_types: List[str]
    resolve_topic_needs: bool
    payload_schema: Optional[Mapping[str, Field]]
    payload_schema_cls: Optional[Type[Schema]]
    comment_notification_builder: type
    needs_context: Optional[str]

    @classmethod
    def allowed_reviewers_ref_types(cls) -> List[str]: ...
    @classmethod
    def reviewers_can_be_none(cls) -> bool: ...
    @classmethod
    def entity_needs(cls, entity: Optional[Any]) -> List[Need]: ...
    @classmethod
    def _create_payload_cls(cls): ...
    @classmethod
    def _create_marshmallow_schema(cls) -> type[Schema]: ...
    @classmethod
    def marshmallow_schema(cls) -> type[Schema]: ...
    def _update_link_config(self, **context_values) -> Dict[str, Any]: ...
    def generate_request_number(self, request: Request, **kwargs) -> str: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
