from typing import Any, Dict, Mapping, Optional

from invenio_communities.members.records.api import Member
from invenio_communities.members.services.fields import RoleField as RoleField
from marshmallow import Schema, fields, validates_schema
from marshmallow_utils.fields import TZDateTime

class MemberEntitySchema(Schema):
    type: fields.String
    id: fields.String
    is_current_user: fields.Boolean

class MembersSchema(Schema):
    members: fields.List

class RequestSchema(Schema):
    id: fields.String
    status: fields.String
    is_open: fields.Boolean
    expires_at: fields.String

class AddBulkSchema(MembersSchema, Schema):
    role: RoleField
    visible: fields.Boolean

class InviteBulkSchema(AddBulkSchema):
    message: fields.String

class UpdateBulkSchema(MembersSchema, Schema):
    role: RoleField
    visible: fields.Boolean
    @validates_schema
    def validate_schema(self, data: Mapping[str, Any], **kwargs) -> None: ...

class DeleteBulkSchema(MembersSchema): ...

class RequestMembershipSchema(Schema):
    message: fields.String

class PublicDumpSchema(Schema):
    id: fields.String
    member: fields.Method
    def get_member(self, obj: Member) -> Optional[Dict[str, str]]: ...
    def get_user_member(self, user: Mapping[str, Any]) -> Dict[str, str]: ...
    def get_group_member(self, group: Mapping[str, Any]) -> Dict[str, str]: ...

class MemberDumpSchema(PublicDumpSchema):
    role: fields.String
    visible: fields.Boolean
    is_current_user: fields.Method
    permissions: fields.Method
    created: TZDateTime
    updated: TZDateTime
    revision_id: fields.Int
    def is_self(self, obj: Member) -> bool: ...
    def get_current_user(self, obj: Member) -> bool: ...
    def get_permissions(self, obj: Member) -> Dict[str, bool]: ...

class InvitationDumpSchema(MemberDumpSchema):
    request: fields.Nested
    permissions: fields.Method
    def get_permissions(self, obj: Mapping[str, Any]) -> Dict[str, bool]: ...
