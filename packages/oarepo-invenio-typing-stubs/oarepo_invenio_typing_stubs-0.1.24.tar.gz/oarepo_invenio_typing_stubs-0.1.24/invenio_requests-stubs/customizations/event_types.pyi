from typing import Any, Callable, Dict, Optional, Union

from invenio_requests.proxies import current_requests as current_requests
from marshmallow import fields
from marshmallow.schema import Schema

class EventType:
    type_id: Optional[str]
    payload_schema: Optional[
        Union[Dict[str, fields.Field], Callable[[], Dict[str, fields.Field]]]
    ]
    payload_required: bool
    payload: Optional[Dict[str, Any]]
    def __init__(self, payload: Optional[Dict[str, Any]] = None) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @classmethod
    def _create_marshmallow_schema(cls) -> type[Schema]: ...
    @classmethod
    def marshmallow_schema(cls) -> type[Schema]: ...

class LogEventType(EventType):
    @staticmethod
    def payload_schema() -> Dict[str, fields.Field]: ...

class ReviewersUpdatedType(EventType):
    @staticmethod
    def payload_schema() -> Dict[str, fields.Field]: ...

class CommentEventType(EventType):
    @staticmethod
    def payload_schema() -> Dict[str, fields.Field]: ...
    payload_required: bool
