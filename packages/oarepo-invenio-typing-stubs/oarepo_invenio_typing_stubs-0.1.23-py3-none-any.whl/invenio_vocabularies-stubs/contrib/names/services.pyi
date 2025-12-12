from typing import Generic, TypeVar

from invenio_records_resources.services.records.config import RecordServiceConfig
from invenio_records_resources.services.records.service import RecordService
from invenio_vocabularies.contrib.names.names import record_type as record_type

NamesServiceConfig: type[RecordServiceConfig]

C = TypeVar("C", bound=RecordServiceConfig)

class NamesService(RecordService[C], Generic[C]):
    def resolve(self, identity, id_, id_type, many: bool = False): ...
