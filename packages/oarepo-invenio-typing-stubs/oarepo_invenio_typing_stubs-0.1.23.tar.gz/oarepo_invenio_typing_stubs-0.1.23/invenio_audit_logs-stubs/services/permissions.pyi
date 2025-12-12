from invenio_records_permissions.generators import Generator
from invenio_records_permissions.policies import BasePermissionPolicy

class AuditLogPermissionPolicy(BasePermissionPolicy):
    # NOTE: use tuples so the base definitions stay immutable while subclasses can
    # override the attribute with their own generator sequence.
    can_search: tuple[Generator, ...]
    can_create: tuple[Generator, ...]
    can_read: tuple[Generator, ...]
    can_update: tuple[Generator, ...]
    can_delete: tuple[Generator, ...]
