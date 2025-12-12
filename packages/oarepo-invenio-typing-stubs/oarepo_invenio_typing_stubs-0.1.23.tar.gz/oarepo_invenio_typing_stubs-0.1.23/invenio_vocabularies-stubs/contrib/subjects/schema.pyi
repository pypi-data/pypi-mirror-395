from typing import Any

from invenio_vocabularies.contrib.subjects.config import (
    subject_schemes as subject_schemes,
)
from invenio_vocabularies.services.schema import (
    BaseVocabularySchema as BaseVocabularySchema,
)
from invenio_vocabularies.services.schema import (
    ContribVocabularyRelationSchema as ContribVocabularyRelationSchema,
)
from invenio_vocabularies.services.schema import i18n_strings as i18n_strings
from marshmallow import EXCLUDE, fields, pre_load
from marshmallow import Schema as Schema
from marshmallow import validate as validate
from marshmallow_utils.fields import URL as URL

class StringOrListOfStrings(fields.Field): ...

class SubjectSchema(BaseVocabularySchema):
    id: Any
    scheme: Any
    subject: Any
    title = i18n_strings
    props: Any
    identifiers: Any
    synonyms: Any
    @pre_load
    def add_subject_from_title(self, data, **kwargs): ...

class SubjectRelationSchema(ContribVocabularyRelationSchema):
    class Meta:
        unknown = EXCLUDE

    ftf_name: str
    parent_field_name: str
    subject: Any
    scheme: Any
    title: Any
    props: Any
    identifiers: Any
    synonyms: Any
