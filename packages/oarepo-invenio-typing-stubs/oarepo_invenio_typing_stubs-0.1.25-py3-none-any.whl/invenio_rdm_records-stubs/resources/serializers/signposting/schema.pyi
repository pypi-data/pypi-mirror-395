from __future__ import annotations

from typing import Any, Mapping

import idutils as idutils
from invenio_base import invenio_url_for as invenio_url_for
from invenio_rdm_records.resources.serializers.utils import (
    get_vocabulary_props as get_vocabulary_props,
)
from marshmallow import Schema as Schema
from marshmallow import fields as fields
from marshmallow import missing as missing
from marshmallow import post_dump as post_dump

class LandingPageSchema(Schema):
    author: fields.Method
    cite_as: fields.Method
    describedby: fields.Method
    item: fields.Method
    license: fields.Method
    type: fields.Method
    def serialize_author(self, obj: Mapping[str, Any], **kwargs: Any): ...
    def serialize_cite_as(self, obj: Mapping[str, Any], **kwargs: Any): ...
    def serialize_describedby(self, obj: Mapping[str, Any], **kwargs: Any): ...
    def serialize_item(self, obj: Mapping[str, Any], **kwargs: Any): ...
    def serialize_license(self, obj: Mapping[str, Any], **kwargs: Any): ...
    def serialize_type(self, obj: Mapping[str, Any], **kwargs: Any): ...

class LandingPageLvl1Schema(LandingPageSchema):
    linkset: fields.Method
    def serialize_linkset(self, obj: Mapping[str, Any], **kwargs: Any): ...
    @post_dump
    def fallback_to_lvl2_linkset_only_if_collections_too_big(
        self, data: Mapping[str, Any], **kwargs: Any
    ): ...

class LandingPageLvl2Schema(LandingPageSchema):
    anchor: fields.Method
    def serialize_anchor(self, obj: Mapping[str, Any], **kwargs: Any): ...

class ContentResourceSchema(Schema):
    anchor: fields.Method
    collection: fields.Method
    def serialize_anchor(self, obj: Mapping[str, Any], **kwargs: Any): ...
    def serialize_collection(self, obj: Mapping[str, Any], **kwargs: Any): ...

class MetadataResourceSchema(Schema):
    anchor: fields.Method
    describes: fields.Method
    def serialize_anchor(self, obj: Mapping[str, Any], **kwargs: Any): ...
    def serialize_describes(self, obj: Mapping[str, Any], **kwargs: Any): ...

class FAIRSignpostingProfileLvl2Schema(Schema):
    linkset: fields.Method
    def serialize_linkset(self, obj: Mapping[str, Any], **kwargs: Any): ...
