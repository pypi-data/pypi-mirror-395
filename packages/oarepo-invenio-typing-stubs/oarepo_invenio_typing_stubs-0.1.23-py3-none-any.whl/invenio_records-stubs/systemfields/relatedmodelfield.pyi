from typing import Any, Callable, Optional, Type, overload

from invenio_records.api import Record
from invenio_records.systemfields.base import SystemField, SystemFieldContext

class RelatedModelFieldContext[R: Record = Record](SystemFieldContext):
    def session_merge(self, record: R) -> None: ...

class RelatedModelField(SystemField):
    _model: Type[Any]
    _required: bool
    _load: Callable[..., Optional[Any]]
    _dump: Callable[..., None]
    _context_cls: Type[RelatedModelFieldContext]

    def __init__(
        self,
        model: Type[Any],
        key: Optional[str] = ...,
        required: bool = ...,
        load: Optional[Callable[..., Optional[Any]]] = ...,
        dump: Optional[Callable[..., None]] = ...,
        context_cls: Optional[Type[RelatedModelFieldContext]] = ...,
    ): ...
    def pre_commit(self, record: Record) -> None: ...
    def obj(self, record: Record) -> Optional[Any]: ...
    def set_obj(self, record: Record, obj: Any) -> None: ...
    @overload  # type: ignore[override] # not consistent with systemfield
    def __get__(  # type: ignore[override] # not consistent with systemfield
        self, instance: None, owner: type[Record]
    ) -> RelatedModelFieldContext: ...
    @overload
    def __get__(self, instance: Record, owner: type[Record]) -> Any: ...  # type: ignore[override] # not consistent with systemfield
    def __set__(self, instance: Record, value: Any) -> None: ...  # type: ignore[override]
