from typing import Optional, Self, Union, overload

from invenio_records.systemfields import SystemField
from invenio_records_resources.records.api import Record
from invenio_search.engine import dsl

class IndexField(SystemField):  # type: ignore[misc]
    _index: dsl.Index
    search_alias: Optional[str]  # keep typing as it is defined in constructor

    def __init__(
        self,
        index_or_alias: Union[dsl.Index, str],
        search_alias: Optional[str | list[str] | tuple[str]] = None,
    ) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Record, owner: type[Record]
    ) -> dsl.Index: ...
    def __set__(self, instance: Record, value: dsl.Index) -> None: ...  # type: ignore[override]
