from typing import Type

from invenio_records_resources.resources import RecordResource, RecordResourceConfig
from invenio_vocabularies.contrib.affiliations.affiliations import (
    record_type as record_type,
)

AffiliationsResourceConfig: Type[RecordResourceConfig]
AffiliationsResource: Type[RecordResource]
