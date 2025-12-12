from typing import Any, Dict

from flask import Flask
from invenio_audit_logs import config as config
from invenio_audit_logs.resources import AuditLogResource as AuditLogResource
from invenio_audit_logs.resources import (
    AuditLogResourceConfig as AuditLogResourceConfig,
)
from invenio_audit_logs.services import AuditLogService as AuditLogService
from invenio_audit_logs.services import AuditLogServiceConfig as AuditLogServiceConfig

class InvenioAuditLogs:
    """Invenio-Audit-Logs extension."""

    audit_log_service: AuditLogService
    audit_log_resource: AuditLogResource
    actions_registry: Dict[str, Any]

    def __init__(self, app: Flask | None = None) -> None: ...
    def init_app(self, app: Flask) -> None: ...
    def init_config(self, app: Flask) -> None: ...
    def init_services(self, app: Flask) -> None: ...
    def init_resources(self, app: Flask) -> None: ...
    def load_actions_registry(self) -> None: ...
