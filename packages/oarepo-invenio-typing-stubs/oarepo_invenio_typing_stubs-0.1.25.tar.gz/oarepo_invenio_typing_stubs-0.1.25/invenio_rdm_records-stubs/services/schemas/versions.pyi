from __future__ import annotations

from marshmallow import Schema

class VersionsSchema(Schema):
    field_dump_permissions: dict[str, str]
