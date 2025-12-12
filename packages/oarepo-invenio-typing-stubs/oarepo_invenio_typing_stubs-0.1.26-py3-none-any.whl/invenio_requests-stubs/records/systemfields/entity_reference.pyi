from functools import partial
from typing import Any, Callable

from invenio_records_resources.records.systemfields.entity_reference import (
    MultiReferenceEntityField,
    ReferencedEntityField,
)
from invenio_requests.resolvers.registry import ResolverRegistry as ResolverRegistry

EntityReferenceField: partial[ReferencedEntityField]
check_allowed_creators: partial[Callable[..., Any]]
check_allowed_receivers: partial[Callable[..., Any]]
check_allowed_topics: partial[Callable[..., Any]]
check_allowed_reviewers: partial[Callable[..., Any]]
MultiEntityReferenceField: partial[MultiReferenceEntityField]
