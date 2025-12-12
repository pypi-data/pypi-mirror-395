from typing import Type

from invenio_records_permissions.generators import Generator
from invenio_records_permissions.policies.base import BasePermissionPolicy

def obj_or_import_string(value, default=None): ...

class RecordPermissionPolicy(BasePermissionPolicy):
    NEED_LABEL_TO_ACTION: dict[str, str]
    # NOTE: tuples keep the defaults immutable at this layer while subclasses
    # can provide alternate generator tuples.
    can_read_files: tuple[Generator, ...]
    can_update_files: tuple[Generator, ...]
    can_read_deleted_files: tuple[Generator, ...]
    can_create_or_update_many: tuple[Generator, ...]
    original_action: str
    def __init__(self, action: str, **over) -> None: ...

def get_record_permission_policy() -> Type[RecordPermissionPolicy]: ...
