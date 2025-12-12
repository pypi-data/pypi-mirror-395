from invenio_records_resources.references.entity_resolvers import (
    EntityResolver as EntityResolver,
)
from invenio_records_resources.references.entity_resolvers import (
    RecordResolver as RecordResolver,
)
from invenio_records_resources.references.grants import EntityGrant as EntityGrant
from invenio_records_resources.references.registry import (
    ResolverRegistryBase as ResolverRegistryBase,
)

__all__ = (
    "EntityGrant",
    "EntityResolver",
    "RecordResolver",
    "ResolverRegistryBase",
)
