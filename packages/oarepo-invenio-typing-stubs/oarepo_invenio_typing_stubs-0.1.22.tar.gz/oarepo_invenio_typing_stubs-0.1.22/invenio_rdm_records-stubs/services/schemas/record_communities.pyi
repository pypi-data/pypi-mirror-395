from __future__ import annotations

from marshmallow import Schema
from marshmallow import fields as fields

class CommunitySchema(Schema):
    id: fields.String
    comment: fields.String
    require_review: fields.Boolean

class RecordCommunitiesSchema(Schema):
    communities: fields.List
    def validate_communities(self, value): ...
