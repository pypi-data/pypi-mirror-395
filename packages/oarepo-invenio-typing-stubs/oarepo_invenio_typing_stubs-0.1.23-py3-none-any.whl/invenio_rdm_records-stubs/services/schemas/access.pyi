from __future__ import annotations

from marshmallow import Schema
from marshmallow import fields as fields
from marshmallow_utils.fields import ISODateString, SanitizedUnicode
from marshmallow_utils.fields.nestedattr import NestedAttribute

class EmbargoSchema(Schema):
    active: fields.Boolean
    until: ISODateString
    reason: SanitizedUnicode
    def validate_embargo(self, data, **kwargs): ...

class AccessSchema(Schema):
    record: SanitizedUnicode
    files: SanitizedUnicode
    embargo: NestedAttribute
    status: SanitizedUnicode
    def validate_protection_value(self, value, field_name): ...
    def get_attribute(self, obj, attr, default): ...
    def validate_record_protection(self, value, data_key=None): ...
    def validate_files_protection(self, value, data_key=None): ...
