from typing import Any, Dict

from marshmallow import Schema, fields, post_load, pre_load

class MinimalCommunitySchema(Schema):
    slug: fields.String
    title: fields.String
    @post_load
    def load_default(self, data: Dict[str, str], **kwargs) -> Dict[str, Any]: ...

class SubcommunityRequestSchema(Schema):
    community_id: fields.String
    community: fields.Nested
    @pre_load
    def validate(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]: ...
