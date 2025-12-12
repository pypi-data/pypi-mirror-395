from __future__ import annotations

from marshmallow import Schema
from marshmallow import fields as fields
from marshmallow_utils.fields import SanitizedUnicode

class MetadataSchema(Schema):
    page: fields.Integer
    type: fields.String
    language: fields.String
    encoding: fields.String
    charset: fields.String
    previewer: fields.String
    width: fields.Integer
    height: fields.Integer

class AccessSchema(Schema):
    hidden: fields.Boolean

class ProcessorSchema(Schema):
    type: fields.String
    status: fields.String
    source_file_id: fields.String
    props: fields.Dict

class FileSchema(Schema):
    id: fields.String
    checksum: fields.String
    ext: fields.String
    size: fields.Integer
    mimetype: fields.String
    storage_class: fields.String
    key: SanitizedUnicode
    metadata: fields.Nested
    access: fields.Nested
    processor: fields.Nested

class FilesSchema(Schema):
    field_dump_permissions: dict[str, str]
    enabled: fields.Boolean
    default_preview: SanitizedUnicode
    order: fields.List
    count: fields.Integer
    total_bytes: fields.Integer
    entries: fields.Dict
    def clean(self, data, **kwargs): ...
    def get_attribute(self, obj, attr, default): ...

class MediaFileSchema(FileSchema):
    language: fields.Nested
