from invenio_records_resources.references.entity_resolvers.base import (
    EntityProxy as EntityProxy,
)
from invenio_records_resources.references.entity_resolvers.base import (
    EntityResolver as EntityResolver,
)
from invenio_records_resources.references.entity_resolvers.records import (
    RecordPKProxy as RecordPKProxy,
)
from invenio_records_resources.references.entity_resolvers.records import (
    RecordProxy as RecordProxy,
)
from invenio_records_resources.references.entity_resolvers.records import (
    RecordResolver as RecordResolver,
)
from invenio_records_resources.references.entity_resolvers.results import (
    ServiceResultProxy as ServiceResultProxy,
)
from invenio_records_resources.references.entity_resolvers.results import (
    ServiceResultResolver as ServiceResultResolver,
)

__all__ = (
    "EntityProxy",
    "EntityResolver",
    "RecordPKProxy",
    "RecordProxy",
    "RecordResolver",
    "ServiceResultProxy",
    "ServiceResultResolver",
)
