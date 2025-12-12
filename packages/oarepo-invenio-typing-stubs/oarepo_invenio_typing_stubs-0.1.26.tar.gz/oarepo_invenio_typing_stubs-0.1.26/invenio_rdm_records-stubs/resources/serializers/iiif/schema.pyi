from __future__ import annotations

from typing import Any, Mapping

from flask import current_app as current_app
from marshmallow import Schema as Schema
from marshmallow import fields as fields
from marshmallow import missing as missing
from marshmallow import post_dump as post_dump
from marshmallow import pre_dump as pre_dump

class SelfList(fields.List):
    def get_value(
        self, obj: Mapping[str, Any], attr, accessor=None, default=missing
    ): ...

class SelfNested(fields.Nested):
    def get_value(
        self, obj: Mapping[str, Any], attr, accessor=None, default=missing
    ): ...

class IIIFInfoV2Schema(Schema):
    class Meta:
        include: dict[str, fields.Field]

    protocol: fields.Constant
    profile: fields.Constant
    tiles: fields.Constant
    width: fields.Integer
    height: fields.Integer

class IIIFImageServiceV2Schema(Schema):
    class Meta:
        include: dict[str, fields.Field]

class IIIFImageResourceV2Schema(Schema):
    class Meta:
        include: dict[str, fields.Field]

    format: fields.String
    width: fields.Integer
    height: fields.Integer
    service: SelfNested

class IIIFImageV2Schema(Schema):
    class Meta:
        include: dict[str, fields.Field]

    motivation: fields.Constant
    resource: SelfNested
    on: fields.String

class IIIFCanvasV2Schema(Schema):
    class Meta:
        include: dict[str, fields.Field]

    label: fields.String
    height: fields.Integer
    width: fields.Integer
    images: SelfList

class ListIIIFFilesAttribute(fields.List):
    def get_value(self, obj: Mapping[str, Any], *args: Any, **kwargs: Any): ...

class IIIFSequenceV2Schema(Schema):
    class Meta:
        include: dict[str, fields.Field]

    label: fields.Constant
    viewingDirection: fields.Constant
    viewingHint: fields.Constant
    canvases: ListIIIFFilesAttribute

class IIIFManifestV2Schema(Schema):
    class Meta:
        include: dict[str, fields.Field]

    label: fields.String
    metadata: fields.Method
    description: fields.String
    license: fields.Method
    sequences: SelfList
    def get_license(self, obj: Mapping[str, Any]): ...
    def get_metadata(self, obj: Mapping[str, Any]): ...
    @post_dump
    def sortcanvases(self, manifest: Mapping[str, Any], many, **kwargs): ...
