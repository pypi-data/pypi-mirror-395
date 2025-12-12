from typing import Any, Optional, Self, overload

from invenio_records.api import Record
from invenio_records.systemfields.base import SystemField

class DictField(SystemField):  # type: ignore[misc]
    clear_none: bool
    create_if_missing: bool

    def __init__(
        self,
        key: Optional[str] = ...,
        clear_none: bool = ...,
        create_if_missing: bool = ...,
    ): ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Record, owner: type[Record]
    ) -> dict[str, Any]: ...
    def __set__(self, instance: Record, value: dict[str, Any]) -> None: ...  # type: ignore[override]
