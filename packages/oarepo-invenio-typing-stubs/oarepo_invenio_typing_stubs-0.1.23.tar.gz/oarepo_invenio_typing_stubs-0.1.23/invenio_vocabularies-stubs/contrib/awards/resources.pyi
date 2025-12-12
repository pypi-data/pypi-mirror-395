from typing import Type

from invenio_records_resources.resources import RecordResource, RecordResourceConfig
from invenio_vocabularies.contrib.awards.awards import record_type as record_type

AwardsResourceConfig: Type[RecordResourceConfig]
AwardsResource: Type[RecordResource]
