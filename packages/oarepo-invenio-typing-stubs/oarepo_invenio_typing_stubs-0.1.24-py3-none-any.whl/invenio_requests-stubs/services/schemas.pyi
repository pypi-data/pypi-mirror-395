from typing import Any, Dict, Optional

from invenio_records_resources.services.records.schema import BaseRecordSchema
from invenio_requests.customizations.event_types import (
    CommentEventType as CommentEventType,
)
from invenio_requests.customizations.event_types import EventType as EventType
from invenio_requests.proxies import (
    current_event_type_registry as current_event_type_registry,
)
from invenio_requests.proxies import current_requests as current_requests
from invenio_requests.records.api import RequestEvent
from marshmallow import INCLUDE as INCLUDE
from marshmallow import RAISE, fields
from marshmallow import Schema as Schema
from marshmallow import ValidationError as ValidationError
from marshmallow import post_dump as post_dump
from marshmallow import post_load as post_load
from marshmallow import validate as validate

class RequestSchema(BaseRecordSchema):
    type: fields.String
    title: fields.String
    description: fields.String
    number: fields.String
    status: fields.String
    is_closed: fields.Boolean
    is_open: fields.Boolean
    expires_at: fields.DateTime
    is_expired: fields.Boolean

    class Meta:
        unknown = RAISE

class GenericRequestSchema(RequestSchema):
    created_by: fields.Dict
    receiver: fields.Dict
    topic: fields.Dict

class EventTypeMarshmallowField(fields.Str):
    def _serialize(
        self, value: Any, attr: Optional[str], obj: Any, **kwargs: Any
    ) -> str: ...

class RequestEventSchema(BaseRecordSchema):
    type: EventTypeMarshmallowField
    created_by: fields.Dict
    permissions: fields.Method

    def get_permissions(self, obj: RequestEvent) -> Dict[str, bool]: ...
