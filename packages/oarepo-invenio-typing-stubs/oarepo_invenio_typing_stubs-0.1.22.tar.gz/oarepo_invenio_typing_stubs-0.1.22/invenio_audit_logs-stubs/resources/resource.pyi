from typing import Generic, TypeVar

from invenio_audit_logs.resources.config import AuditLogResourceConfig
from invenio_audit_logs.services.service import AuditLogService
from invenio_records_resources.resources.records.resource import (
    RecordResource,
    request_extra_args,
    request_search_args,
    request_view_args,
)

C = TypeVar("C", bound=AuditLogResourceConfig)
S = TypeVar("S", bound=AuditLogService)

class AuditLogResource(RecordResource[C, S], Generic[C, S]):
    def create_blueprint(self, **options): ...
    def create_url_rules(self): ...
    @request_extra_args
    @request_search_args
    @request_view_args
    def search(self): ...
    @request_extra_args
    @request_view_args
    def read(self): ...
