from typing import Generic, TypeVar

from invenio_audit_logs.services.config import AuditLogServiceConfig
from invenio_audit_logs.services.uow import (
    AuditRecordCommitOp as AuditRecordCommitOp,
)
from invenio_records_resources.services.records.service import RecordService

C = TypeVar("C", bound=AuditLogServiceConfig)

class AuditLogService(RecordService[C], Generic[C]):
    pass
