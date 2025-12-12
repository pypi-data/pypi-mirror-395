from __future__ import annotations

from marshmallow import Schema
from marshmallow import fields as fields

class QuotaSchema(Schema):
    quota_size: fields.Integer
    max_file_size: fields.Integer
    notes: fields.String
