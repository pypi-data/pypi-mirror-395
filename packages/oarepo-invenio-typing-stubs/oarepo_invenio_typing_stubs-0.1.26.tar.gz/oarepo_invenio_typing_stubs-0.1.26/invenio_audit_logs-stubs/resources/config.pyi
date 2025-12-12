from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin

class AuditLogSearchRequestArgsSchema(SearchRequestArgsSchema): ...
class AuditLogResourceConfig(RecordResourceConfig, ConfiguratorMixin): ...
