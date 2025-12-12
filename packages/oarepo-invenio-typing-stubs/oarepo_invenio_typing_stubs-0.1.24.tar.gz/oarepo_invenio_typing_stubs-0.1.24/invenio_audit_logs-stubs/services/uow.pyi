from typing import Any

from flask_principal import Identity
from invenio_access.permissions import system_identity
from invenio_audit_logs.proxies import (
    current_audit_logs_service as current_audit_logs_service,
)
from invenio_db.uow import Operation, UnitOfWork
from invenio_records_resources.services.uow import RecordCommitOp

class AuditLogOp(Operation):
    data: dict[str, Any]
    identity: Identity
    result: Any
    def __init__(
        self, data: dict[str, Any], identity: Identity = system_identity
    ) -> None: ...
    def on_register(self, uow: UnitOfWork) -> None: ...

class AuditRecordCommitOp(RecordCommitOp):
    def on_commit(self, uow: UnitOfWork) -> Any: ...
