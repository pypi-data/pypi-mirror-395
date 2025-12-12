from typing import Any, List, Self, Union, overload

from invenio_pidstore.models import PIDStatus  # type: ignore[import-untyped]
from invenio_records.dumpers import Dumper
from invenio_records.systemfields import SystemField
from invenio_records_resources.records.api import Record

class PIDStatusCheckField(SystemField):  # type: ignore[misc]
    _pid_status: List[PIDStatus]
    _dump: bool

    def __init__(
        self,
        key: str = ...,
        status: Union[PIDStatus, List[PIDStatus], None] = ...,
        dump: bool = ...,
    ) -> None: ...
    def pre_dump(
        self, record: Record, data: dict[str, Any], dumper: Any | None = ...
    ) -> None: ...
    def pre_load(
        self, data: dict[str, Any], loader: Dumper | None = ..., **kwargs: Any
    ) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Record, owner: type[Record]
    ) -> bool: ...
    def __set__(self, instance: Record, value: bool) -> None: ...  # type: ignore[override]
