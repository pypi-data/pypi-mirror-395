from typing import Any, Dict, Optional

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema, fields, pre_load, validates_schema
from marshmallow_utils.fields import SanitizedUnicode

i18n_strings: fields.Dict

class BaseVocabularyRelationSchema(Schema):
    id: SanitizedUnicode
    administration_schema_type: str

class VocabularyRelationSchema(BaseVocabularyRelationSchema):
    title: fields.Dict
    @pre_load
    def clean(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]: ...

class ContribVocabularyRelationSchema(Schema):
    id: SanitizedUnicode
    ftf_name: Optional[str]
    parent_field_name: Optional[str]
    administration_schema_type: str
    @validates_schema
    def validate_relation_schema(self, data: Dict[str, Any], **kwargs: Any) -> None: ...

class BaseVocabularySchema(BaseRecordSchema):
    title = i18n_strings
    description = i18n_strings
    icon: fields.Str
    tags: fields.List
    administration_schema_type: str

class VocabularySchema(BaseVocabularySchema):
    props: fields.Dict
    type: fields.Str

class ModePIDFieldVocabularyMixin:
    @validates_schema
    def validate_id(self, data: Dict[str, Any], **kwargs: Any) -> None: ...
    def move_id(self, data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]: ...
    def extract_pid_value(
        self, data: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]: ...

class DatastreamObject(Schema):
    type: fields.Str
    args: fields.Dict

class TaskSchema(Schema):
    readers: fields.List
    transformers: fields.List
    writers: fields.List
