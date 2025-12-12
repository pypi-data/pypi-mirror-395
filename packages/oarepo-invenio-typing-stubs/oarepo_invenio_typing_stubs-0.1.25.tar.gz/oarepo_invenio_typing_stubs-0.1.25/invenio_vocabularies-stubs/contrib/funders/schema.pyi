from typing import Any, Dict

from invenio_vocabularies.contrib.funders.config import funder_schemes as funder_schemes
from invenio_vocabularies.services.schema import (
    BaseVocabularySchema as BaseVocabularySchema,
)
from invenio_vocabularies.services.schema import (
    ContribVocabularyRelationSchema as ContribVocabularyRelationSchema,
)
from marshmallow import fields, validates_schema

class FunderRelationSchema(ContribVocabularyRelationSchema):
    ftf_name: str
    parent_field_name: str
    name: Any

class FunderSchema(BaseVocabularySchema):
    name: Any
    country: Any
    country_name: Any
    location_name: Any
    identifiers: Any
    id: Any
    acronym: Any
    aliases: fields.List
    status: Any
    types: fields.List
    @validates_schema
    def validate_id(self, data: Dict[str, Any], **kwargs) -> None: ...
    def move_id(self, data: Dict[str, Any], **kwargs): ...
    def extract_pid_value(self, data: Dict[str, Any], **kwargs): ...
