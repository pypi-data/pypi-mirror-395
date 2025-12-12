from invenio_records_permissions import BasePermissionPolicy
from invenio_records_permissions.generators import Generator

class OAIPMHServerPermissionPolicy(BasePermissionPolicy):
    # NOTE: tuples keep the base class defaults immutable but still let
    # subclasses override them with different generator tuples.
    can_read: tuple[Generator, ...]
    can_create: tuple[Generator, ...]
    can_delete: tuple[Generator, ...]
    can_update: tuple[Generator, ...]
    can_read_format: tuple[Generator, ...]
