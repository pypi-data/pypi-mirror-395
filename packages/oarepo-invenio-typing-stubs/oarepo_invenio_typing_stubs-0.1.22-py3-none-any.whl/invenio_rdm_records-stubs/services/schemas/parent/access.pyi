from typing import ClassVar

from marshmallow import Schema, fields
from marshmallow_utils.permissions import FieldPermissionsMixin

class GrantSubject(Schema):
    id: fields.String
    type: fields.String

class Grant(Schema):
    permission: fields.String
    subject: fields.Nested
    origin: fields.String
    message: fields.Field
    notify: fields.Bool

class Grants(Schema):
    grants: fields.List

class SecretLink(Schema):
    id: fields.String
    created_at: fields.Field
    expires_at: fields.Field
    permission: fields.String
    description: fields.Field
    origin: fields.String
    token: fields.Field

class Agent(Schema):
    user: fields.String

class AccessSettingsSchema(Schema):
    allow_user_requests: fields.Boolean
    allow_guest_requests: fields.Boolean
    accept_conditions_text: fields.Field
    secret_link_expiration: fields.Integer

class ParentAccessSchema(Schema, FieldPermissionsMixin):
    field_dump_permissions: ClassVar[dict[str, str]]

    grants: fields.List
    owned_by: fields.Nested
    links: fields.List
    settings: fields.Nested

class RequestAccessSchema(Schema):
    permission: fields.Constant
    email: fields.Email
    full_name: fields.Field
    message: fields.Field
    consent_to_share_personal_data: fields.String
