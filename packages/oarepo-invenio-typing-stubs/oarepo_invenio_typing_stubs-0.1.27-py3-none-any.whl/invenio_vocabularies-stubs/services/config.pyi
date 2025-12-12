from typing import Any, Dict

import marshmallow as ma
from invenio_indexer.api import RecordIndexer
from invenio_records_resources.records import Record
from invenio_records_resources.services import RecordServiceConfig, SearchOptions
from invenio_vocabularies.records.api import Vocabulary as Vocabulary
from invenio_vocabularies.records.models import VocabularyType as VocabularyType
from invenio_vocabularies.services import results as results
from invenio_vocabularies.services.components import PIDComponent as PIDComponent
from invenio_vocabularies.services.components import (
    VocabularyTypeComponent as VocabularyTypeComponent,
)
from invenio_vocabularies.services.permissions import (
    PermissionPolicy as PermissionPolicy,
)
from invenio_vocabularies.services.schema import TaskSchema as TaskSchema
from invenio_vocabularies.services.schema import VocabularySchema as VocabularySchema

def is_custom_vocabulary_type(vocabulary_type, context): ...

class VocabularySearchOptions(SearchOptions): ...

class VocabularyTypeSearchOptions(SearchOptions):
    sort_direction_options: Dict[str, Dict[str, Any]]
    sort_direction_default: str

class VocabulariesServiceConfig(
    RecordServiceConfig[
        Vocabulary,
        VocabularySearchOptions,
        VocabularySchema,
        RecordIndexer,
        PermissionPolicy,
    ]
):
    task_schema: type[TaskSchema]

class VocabularyTypesServiceConfig(
    RecordServiceConfig[
        Record,
        VocabularyTypeSearchOptions,
        ma.Schema,
        RecordIndexer,
        PermissionPolicy,
    ]
): ...
