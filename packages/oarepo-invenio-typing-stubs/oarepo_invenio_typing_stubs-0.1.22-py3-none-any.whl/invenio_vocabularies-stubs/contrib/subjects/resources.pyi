from invenio_records_resources.resources import RecordResource, RecordResourceConfig
from invenio_vocabularies.contrib.subjects.subjects import record_type as record_type

SubjectsResourceConfig: type[RecordResourceConfig]
SubjectsResource: type[RecordResource]
