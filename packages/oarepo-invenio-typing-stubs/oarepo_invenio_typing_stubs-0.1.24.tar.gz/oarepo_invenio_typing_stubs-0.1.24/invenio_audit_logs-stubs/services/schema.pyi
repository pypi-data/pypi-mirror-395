from typing import Any, ClassVar

from marshmallow import EXCLUDE, Schema, fields, pre_dump, pre_load

class ResourceSchema(Schema):
    type: ClassVar[fields.Str]
    id: ClassVar[fields.Str]

class MetadataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    ip_address: ClassVar[fields.Str]
    session: ClassVar[fields.Str]
    request_id: ClassVar[fields.Str]
    parent_pid: ClassVar[fields.Str]
    revision_id: ClassVar[fields.Int]

class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id: ClassVar[fields.Str]
    username: ClassVar[fields.Str]
    email: ClassVar[fields.Email]

    @pre_load
    def serialize_user(self, obj: Any, **kwargs: Any) -> dict[str, Any]: ...

class AuditLogSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id: ClassVar[fields.Str]
    created: ClassVar[fields.DateTime]
    action: ClassVar[fields.Str]
    resource: ClassVar[fields.Nested]
    metadata: ClassVar[fields.Nested]
    user: ClassVar[fields.Nested]
    # Load-only fields for DB insert
    user_id: ClassVar[fields.Str]
    resource_type: ClassVar[fields.Str]

    @pre_dump
    def add_timestamp(self, obj: Any, **kwargs: Any) -> Any: ...
