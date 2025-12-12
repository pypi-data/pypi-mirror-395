from invenio_records_resources.services.records.config import RecordServiceConfig
from invenio_records_resources.services.records.service import RecordService
from invenio_vocabularies.contrib.funders.funders import record_type as record_type

FundersServiceConfig: type[RecordServiceConfig]
FundersService: type[RecordService]
