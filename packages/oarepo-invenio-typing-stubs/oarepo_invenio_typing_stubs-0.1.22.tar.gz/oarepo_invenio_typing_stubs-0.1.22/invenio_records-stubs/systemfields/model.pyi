from typing import Any, Optional, Self, overload

from invenio_records.api import Record
from invenio_records.systemfields.base import SystemField

class ModelField(SystemField):  # type: ignore[misc]
    _model_field_name: Optional[str]
    dump: bool
    _dump_key: Optional[str]
    _dump_type: Optional[Any]

    def __init__(
        self,
        model_field_name: Optional[str] = ...,
        dump: bool = ...,
        dump_key: Optional[str] = ...,
        dump_type: Optional[Any] = ...,
        **kwargs: Any,
    ): ...
    def _set(self, model: Any, value: Any) -> None: ...
    @property
    def dump_key(self) -> str: ...
    @property
    def dump_type(self) -> Optional[Any]: ...
    @property
    def model_field_name(self) -> str: ...
    def post_init(
        self,
        record: Record,
        data: dict[str, Any],
        model: Any | None = ...,
        **kwargs: Any,
    ) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Record, owner: type[Record]
    ) -> Any: ...
    def __set__(self, instance: Record, value: Any) -> None: ...  # type: ignore[override]
