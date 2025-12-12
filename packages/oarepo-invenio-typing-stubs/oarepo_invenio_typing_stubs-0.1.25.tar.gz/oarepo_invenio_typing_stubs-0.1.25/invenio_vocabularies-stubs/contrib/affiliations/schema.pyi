from invenio_vocabularies.contrib.affiliations.config import (
    affiliation_schemes as affiliation_schemes,
)
from invenio_vocabularies.services.schema import (
    BaseVocabularySchema as BaseVocabularySchema,
)
from invenio_vocabularies.services.schema import (
    ContribVocabularyRelationSchema as ContribVocabularyRelationSchema,
)
from invenio_vocabularies.services.schema import (
    ModePIDFieldVocabularyMixin as ModePIDFieldVocabularyMixin,
)
from marshmallow import fields
from marshmallow_utils.fields import IdentifierSet, SanitizedUnicode

class AffiliationSchema(BaseVocabularySchema, ModePIDFieldVocabularyMixin):
    acronym: SanitizedUnicode
    identifiers: IdentifierSet
    name: SanitizedUnicode
    country: SanitizedUnicode
    country_name: SanitizedUnicode
    location_name: SanitizedUnicode
    id: SanitizedUnicode
    aliases: fields.List
    status: SanitizedUnicode
    types: fields.List

class AffiliationRelationSchema(ContribVocabularyRelationSchema):
    ftf_name: str | None
    parent_field_name: str | None
    name: SanitizedUnicode
    identifiers: IdentifierSet
