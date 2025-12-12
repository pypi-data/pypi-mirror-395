from typing import ClassVar

from invenio_records.dumpers import Dumper
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import ConstantField, DictField, RelatedModelField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField, PIDField
from invenio_vocabularies.records.models import VocabularyMetadata as VocabularyMetadata
from invenio_vocabularies.records.models import VocabularyType as VocabularyType
from invenio_vocabularies.records.pidprovider import (
    VocabularyIdProvider as VocabularyIdProvider,
)
from invenio_vocabularies.records.systemfields import (
    VocabularyPIDFieldContext as VocabularyPIDFieldContext,
)

class Vocabulary(Record):
    model_cls: ClassVar[type[RecordMetadata]]
    schema: ClassVar[ConstantField]
    index: ClassVar[IndexField]
    metadata: ClassVar[DictField]
    type: ClassVar[RelatedModelField]
    pid: ClassVar[PIDField]
    dumper: ClassVar[Dumper]
