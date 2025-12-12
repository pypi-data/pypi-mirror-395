from __future__ import annotations

from typing import Any

from marshmallow import Schema
from marshmallow import fields as fields
from marshmallow_utils.fields import (
    EDTFDateTimeString,
    NestedAttribute,
    SanitizedHTML,
    SanitizedUnicode,
)

def validate_scheme(scheme) -> None: ...

class InternalNoteSchema(Schema):
    id: SanitizedUnicode
    timestamp: EDTFDateTimeString
    added_by: fields.Nested
    note: SanitizedHTML

    class Meta:
        unknown: Any

class RDMRecordSchema(Schema):
    pids: fields.Dict
    metadata: NestedAttribute
    custom_fields: NestedAttribute
    access: NestedAttribute
    files: NestedAttribute
    media_files: NestedAttribute
    revision: fields.Integer
    versions: NestedAttribute
    parent: NestedAttribute
    is_published: fields.Boolean
    status: fields.String
    tombstone: fields.Nested
    deletion_status: fields.Nested
    internal_notes: fields.List
    stats: NestedAttribute
    field_dump_permissions: dict[str, str]
    field_load_permissions: dict[str, str]

    class Meta:
        unknown: Any

    def default_nested(self, data): ...
    def hide_tombstone(self, data): ...
    def post_dump(self, data, many, **kwargs): ...
