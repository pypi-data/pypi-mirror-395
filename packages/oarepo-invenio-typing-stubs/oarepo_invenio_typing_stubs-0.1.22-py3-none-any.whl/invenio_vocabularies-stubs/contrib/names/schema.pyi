from typing import Any, Dict

from invenio_vocabularies.contrib.affiliations.schema import (
    AffiliationRelationSchema as BaseAffiliationRelationSchema,
)
from invenio_vocabularies.contrib.names.config import names_schemes as names_schemes
from invenio_vocabularies.services.schema import (
    BaseVocabularySchema as BaseVocabularySchema,
)
from invenio_vocabularies.services.schema import (
    ModePIDFieldVocabularyMixin as ModePIDFieldVocabularyMixin,
)
from marshmallow import EXCLUDE, fields, post_dump, post_load, validates_schema

class AffiliationRelationSchema(BaseAffiliationRelationSchema):
    acronym: Any

    class Meta:
        unknown = EXCLUDE

class NameSchema(BaseVocabularySchema, ModePIDFieldVocabularyMixin):
    internal_id: Any
    name: Any
    given_name: Any
    family_name: Any
    identifiers: Any
    affiliations: fields.List
    props: fields.Dict
    @validates_schema
    def validate_names(self, data: Dict[str, Any], **kwargs) -> None: ...
    @validates_schema
    def validate_affiliations(self, data: Dict[str, Any], **kwargs) -> None: ...
    @post_load
    def update_name(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]: ...
    @post_dump
    def dump_name(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]: ...
