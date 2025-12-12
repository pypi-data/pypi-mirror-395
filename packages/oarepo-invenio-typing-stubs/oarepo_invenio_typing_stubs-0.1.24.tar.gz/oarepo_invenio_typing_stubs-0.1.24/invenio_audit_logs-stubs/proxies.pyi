from typing import Any

from invenio_audit_logs.services import AuditLogService

current_audit_logs_service: AuditLogService  # intentionally not using a LocalProxy[AuditLogService] here as mypy does not understand it
current_audit_logs_actions_registry: dict[
    str, Any
]  # intentionally not using a LocalProxy[dict[str, Any]] here as mypy does not understand it
current_audit_logs_resolvers: (
    Any  # intentionally not using a LocalProxy[Any] here as mypy does not understand it
)
