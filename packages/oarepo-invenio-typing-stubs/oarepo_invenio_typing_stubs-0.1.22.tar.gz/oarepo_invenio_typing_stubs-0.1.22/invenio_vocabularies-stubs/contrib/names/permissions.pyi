from invenio_records_permissions.generators import Generator as Generator
from invenio_vocabularies.services.generators import IfTags as IfTags
from invenio_vocabularies.services.permissions import (
    PermissionPolicy as PermissionPolicy,
)

class NamesPermissionPolicy(PermissionPolicy):
    # NOTE: tuples keep the defaults immutable in the base policy but subclasses
    # can still override them with their own generator tuples.
    can_search: tuple[Generator, ...]
    can_read: tuple[Generator, ...]
