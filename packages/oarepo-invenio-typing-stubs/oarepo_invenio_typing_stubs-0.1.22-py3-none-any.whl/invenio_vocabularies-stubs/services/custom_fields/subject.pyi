from typing import Any

from invenio_vocabularies.contrib.subjects.api import Subject as Subject
from invenio_vocabularies.contrib.subjects.schema import (
    SubjectRelationSchema as SubjectRelationSchema,
)
from invenio_vocabularies.services.custom_fields.vocabulary import (
    VocabularyCF as VocabularyCF,
)

class SubjectCF(VocabularyCF): ...

SUBJECT_FIELDS_UI: list[dict[str, Any]]
SUBJECT_FIELDS: set[SubjectCF]
