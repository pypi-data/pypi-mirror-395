from typing import Any

from .access import AccessComponent
from .custom_fields import CustomFieldsComponent
from .metadata import MetadataComponent
from .pids import ParentPIDsComponent, PIDsComponent
from .record_deletion import RecordDeletionComponent
from .review import ReviewComponent
from .verified import ContentModerationComponent

DefaultRecordsComponents: list[type[Any]]

__all__ = (
    "AccessComponent",
    "ContentModerationComponent",
    "CustomFieldsComponent",
    "MetadataComponent",
    "PIDsComponent",
    "ParentPIDsComponent",
    "RecordDeletionComponent",
    "ReviewComponent",
    "DefaultRecordsComponents",
)
