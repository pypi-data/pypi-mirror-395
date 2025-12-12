from typing import Type

from invenio_records_resources.resources import RecordResource, RecordResourceConfig
from invenio_vocabularies.contrib.funders.funders import record_type as record_type

FundersResourceConfig: Type[RecordResourceConfig]
FundersResource: Type[RecordResource]
