from __future__ import annotations

from marshmallow import Schema
from marshmallow import fields as fields

class AgentSchema(Schema):
    user: fields.Dict

class RemovalReasonSchema(Schema):
    id: fields.Str

class TombstoneSchema(Schema):
    removal_reason: fields.Nested
    note: fields.Str
    removed_by: fields.Nested
    removal_date: fields.DateTime
    citation_text: fields.Str
    is_visible: fields.Boolean

class DeletionStatusSchema(Schema):
    is_deleted: fields.Boolean
    status: fields.Str
