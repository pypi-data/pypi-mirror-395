from invenio_records_permissions.ext import (
    InvenioRecordsPermissions as InvenioRecordsPermissions,
)
from invenio_records_permissions.policies import (
    BasePermissionPolicy as BasePermissionPolicy,
)
from invenio_records_permissions.policies import (
    RecordPermissionPolicy as RecordPermissionPolicy,
)

__version__: str

__all__: tuple[str, ...] = (
    "__version__",
    "BasePermissionPolicy",
    "InvenioRecordsPermissions",
    "RecordPermissionPolicy",
)
