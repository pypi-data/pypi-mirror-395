from typing import Type

from invenio_records_resources.services.records.config import RecordServiceConfig
from invenio_records_resources.services.records.service import RecordService
from invenio_vocabularies.contrib.awards.awards import record_type as record_type

AwardsServiceConfig: Type[RecordServiceConfig]
AwardsService: Type[RecordService]
