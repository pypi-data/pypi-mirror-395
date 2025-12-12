from invenio_audit_logs.ext import InvenioAuditLogs as InvenioAuditLogs

# Export the same public API as the runtime package
__all__ = ("__version__", "InvenioAuditLogs")

__version__: str
