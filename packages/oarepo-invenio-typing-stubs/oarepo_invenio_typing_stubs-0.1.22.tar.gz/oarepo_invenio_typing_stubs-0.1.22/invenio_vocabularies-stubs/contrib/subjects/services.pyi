from typing import Generic, TypeVar

from invenio_records_resources.services.records.config import RecordServiceConfig
from invenio_records_resources.services.records.service import RecordService
from invenio_vocabularies.contrib.subjects.subjects import record_type as record_type
from invenio_vocabularies.records.models import VocabularyScheme as VocabularyScheme

SubjectsServiceConfig: type[RecordServiceConfig]

C = TypeVar("C", bound=RecordServiceConfig)

class SubjectsService(RecordService[C], Generic[C]):
    def create_scheme(
        self, identity, id_, name: str = "", uri: str = ""
    ) -> VocabularyScheme: ...
