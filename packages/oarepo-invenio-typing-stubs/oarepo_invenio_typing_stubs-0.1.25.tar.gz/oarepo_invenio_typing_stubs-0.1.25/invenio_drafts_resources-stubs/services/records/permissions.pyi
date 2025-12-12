from invenio_records_permissions.generators import Generator
from invenio_records_permissions.policies.records import (
    RecordPermissionPolicy as RecordPermissionPolicyBase,
)

class RecordPermissionPolicy(RecordPermissionPolicyBase):
    # NOTE: tuples keep the defaults immutable at this level while still letting
    # subclasses replace the attribute with their own generators.
    can_create: tuple[Generator, ...]
    can_new_version: tuple[Generator, ...]
    can_edit: tuple[Generator, ...]
    can_publish: tuple[Generator, ...]
    can_read_draft: tuple[Generator, ...]
    can_update_draft: tuple[Generator, ...]
    can_delete_draft: tuple[Generator, ...]
    can_manage_files: tuple[Generator, ...]
