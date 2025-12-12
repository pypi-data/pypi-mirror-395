from _typeshed import Incomplete
from invenio_records.models import RecordMetadataBase

class _Model: ...

class AuditLog(_Model, RecordMetadataBase):
    __tablename__: str
    encoder: Incomplete
    action: Incomplete
    resource_type: Incomplete
    user_id: Incomplete
