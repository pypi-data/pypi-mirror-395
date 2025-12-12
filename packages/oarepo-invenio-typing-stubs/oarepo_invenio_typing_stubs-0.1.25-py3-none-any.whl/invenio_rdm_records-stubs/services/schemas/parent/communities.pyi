from typing import Any, Mapping

from marshmallow import Schema, fields
from invenio_communities.communities.schema import CommunitySchema


class CommunitiesSchema(Schema):
    ids: fields.List
    default: fields.String
    entries: fields.List

    def clear_none_values(self, data: Mapping[str, Any], **kwargs: Any) -> Mapping[str, Any]: ...
