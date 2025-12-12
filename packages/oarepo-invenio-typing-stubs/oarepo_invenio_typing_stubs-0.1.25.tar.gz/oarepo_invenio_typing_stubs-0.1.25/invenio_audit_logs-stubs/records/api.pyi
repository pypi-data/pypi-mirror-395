from typing import ClassVar

from invenio_audit_logs.records.systemfields import ActionField
from invenio_records.dumpers import Dumper
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import DictField, ModelField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField

class AuditLog(Record):
    model_cls: ClassVar[type[RecordMetadata]]
    dumper: ClassVar[Dumper]
    index: IndexField
    action: ActionField
    user_id: ModelField
    user: DictField
    resource_type: ModelField
    resource: DictField
