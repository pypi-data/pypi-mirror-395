from __future__ import annotations

from typing import Any, Mapping

from marshmallow import Schema as Schema
from marshmallow import fields as fields

class GeoJSONSchema(Schema):
    features: fields.Method
    type: fields.Constant
    def get_locations(self, obj: Mapping[str, Any]) -> list[Mapping[str, Any]]: ...
