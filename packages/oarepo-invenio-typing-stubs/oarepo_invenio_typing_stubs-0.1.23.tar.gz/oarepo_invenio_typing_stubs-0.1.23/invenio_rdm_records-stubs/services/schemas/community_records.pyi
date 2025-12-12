from __future__ import annotations

from marshmallow import Schema
from marshmallow import fields as fields

class RecordSchema(Schema):
    id: fields.Str

class CommunityRecordsSchema(Schema):
    records: fields.List
    def validate_records(self, value): ...
