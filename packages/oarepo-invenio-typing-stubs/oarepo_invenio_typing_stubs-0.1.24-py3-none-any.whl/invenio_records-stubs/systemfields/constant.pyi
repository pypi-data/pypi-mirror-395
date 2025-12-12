from typing import Any, Dict, Optional, Self, overload

from invenio_records.api import Record
from invenio_records.systemfields.base import SystemField

class ConstantField(SystemField):  # type: ignore[misc]
    value: Any

    def __init__(
        self,
        key: Optional[str] = ...,
        value: Any = ...,
    ): ...
    def pre_init(
        self,
        record: Record,
        data: Optional[Dict[str, Any]],
        model: Any = ...,
        **kwargs: Any,
    ) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Record, owner: type[Record]
    ) -> Any: ...
    def __set__(self, instance: Record, value: Any) -> None: ...  # type: ignore[override]
