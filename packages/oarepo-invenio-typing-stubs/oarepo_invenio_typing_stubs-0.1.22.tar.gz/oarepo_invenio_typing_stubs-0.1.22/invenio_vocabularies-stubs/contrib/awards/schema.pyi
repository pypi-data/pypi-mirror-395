from invenio_vocabularies.contrib.awards.config import award_schemes as award_schemes
from invenio_vocabularies.contrib.funders.schema import (
    FunderRelationSchema as FunderRelationSchema,
)
from invenio_vocabularies.contrib.subjects.schema import (
    SubjectRelationSchema as SubjectRelationSchema,
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
from invenio_vocabularies.services.schema import i18n_strings as i18n_strings
from marshmallow import Schema, fields, validates_schema
from marshmallow_utils.fields import IdentifierSet, ISODateString, SanitizedUnicode

class AwardOrganizationRelationSchema(ContribVocabularyRelationSchema):
    ftf_name: str | None
    parent_field_name: str | None
    organization: SanitizedUnicode
    scheme: SanitizedUnicode

class AwardSchema(BaseVocabularySchema, ModePIDFieldVocabularyMixin):
    identifiers: IdentifierSet
    number: SanitizedUnicode
    funder: fields.Nested
    acronym: SanitizedUnicode
    program: SanitizedUnicode
    subjects: fields.List
    organizations: fields.List
    start_date: ISODateString
    end_date: ISODateString
    id: SanitizedUnicode

class AwardRelationSchema(Schema):
    id: SanitizedUnicode
    number: SanitizedUnicode
    title = i18n_strings
    identifiers: IdentifierSet
    acronym: SanitizedUnicode
    program: SanitizedUnicode
    @validates_schema
    def validate_data(self, data, **kwargs) -> None: ...

class FundingRelationSchema(Schema):
    funder: fields.Nested
    award: fields.Nested
    @validates_schema
    def validate_data(self, data, **kwargs) -> None: ...
