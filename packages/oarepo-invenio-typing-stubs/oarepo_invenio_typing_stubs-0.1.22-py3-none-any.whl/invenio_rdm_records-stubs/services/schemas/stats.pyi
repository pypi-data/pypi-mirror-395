from __future__ import annotations

from marshmallow import Schema
from marshmallow import fields as fields

class PartialStatsSchema(Schema):
    views: fields.Integer
    unique_views: fields.Integer
    downloads: fields.Integer
    unique_downloads: fields.Integer
    data_volume: fields.Integer

class StatsSchema(Schema):
    this_version: fields.Nested
    all_versions: fields.Nested
