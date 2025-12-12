import uuid
from typing import Any, Callable

from invenio_pidstore.models import PersistentIdentifier  # type: ignore[import-untyped]
from invenio_records_resources.records.api import (
    PersistentIdentifierWrapper,
    Record,
)

class UUIDResolver:
    object_getter: Callable[[uuid.UUID], Record] | None

    def __init__(
        self,
        getter: Callable[[uuid.UUID], Record] | None = None,
        **kwargs: Any,
    ) -> None: ...
    def resolve(
        self, pid_value: str | uuid.UUID
    ) -> tuple[PersistentIdentifier, Record]: ...

class ModelResolver:
    _record_cls: type[Record]
    model_field_name: str

    def __init__(
        self, record_cls: type[Record], model_field_name: str, **kwargs: Any
    ) -> None: ...
    def resolve(
        self, pid_value: str
    ) -> tuple[PersistentIdentifier | PersistentIdentifierWrapper, Record]: ...
