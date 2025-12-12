from collections.abc import Mapping
from typing import Any

from invenio_audit_logs.proxies import (
    current_audit_logs_actions_registry as current_audit_logs_actions_registry,
)
from invenio_audit_logs.records import AuditLog as AuditLog
from invenio_audit_logs.services import results as results
from invenio_audit_logs.services.permissions import (
    AuditLogPermissionPolicy as AuditLogPermissionPolicy,
)
from invenio_audit_logs.services.schema import AuditLogSchema as AuditLogSchema
from invenio_indexer.api import RecordIndexer
from invenio_records.dumpers import Dumper
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_records_resources.services.base.results import (
    ServiceItemResult,
    ServiceListResult,
)
from invenio_records_resources.services.records.config import (
    RecordServiceConfig,
    SearchOptions,
)

class AuditLogSearchOptions(SearchOptions):
    # NOTE: immutable defaults prevent shared-state mutation across configs.
    sort_default: str
    sort_default_no_query: str
    query_parser_cls: Any
    sort_options: Mapping[str, Mapping[str, Any]]
    facets: Mapping[str, Any]
    pagination_options: Mapping[str, int]
    params_interpreters_cls: tuple[Any, ...]

def idvar(log, vars) -> None: ...

class AuditLogServiceConfig(
    RecordServiceConfig[
        AuditLog,
        AuditLogSearchOptions,
        AuditLogSchema,
        RecordIndexer,
        AuditLogPermissionPolicy,
    ],
    ConfiguratorMixin,
):
    # NOTE: configs expose immutable defaults to keep instances isolated.
    enabled: Any
    service_id: str | None
    permission_policy_cls: type[AuditLogPermissionPolicy]
    search: type[AuditLogSearchOptions]
    schema: type[AuditLogSchema] | None
    record_cls: type[AuditLog]
    indexer_cls: type[RecordIndexer]
    indexer_queue_name: str
    index_dumper: Dumper | None
    result_item_cls: type[ServiceItemResult]
    result_list_cls: type[ServiceListResult]
