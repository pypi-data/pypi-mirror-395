from typing import Any, Callable, Iterable, Self

from invenio_search.engine import dsl

class DefaultFilter:
    _query: Any | Callable[[], Any] | None
    query_parser: Callable[[Any], Any]

    def __init__(
        self,
        query: Any | Callable[[], Any] | None = ...,
        query_parser: Callable[[Any], Any] | None = ...,
    ) -> None: ...
    @property
    def query(self) -> Any: ...
    def __get__(self, obj: Any, objtype: type | None) -> Any: ...

class MinShouldMatch(str):
    def __lt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...

class BaseRecordsSearch(dsl.Search):
    class Meta:
        index: str | None
        fields: tuple[str, ...]
        facets: dict[str, Any]
        default_filter: Any | None

    def __init__(self, **kwargs: Any) -> None: ...
    def get_record(self, id_: Any) -> Self: ...
    def get_records(self, ids: Iterable[Any]) -> Self: ...
    @classmethod
    def faceted_search(
        cls,
        query: Any | None = ...,
        filters: dict[str, Any] | None = ...,
        search: "BaseRecordsSearch" | None = ...,
    ) -> dsl.FacetedSearch: ...
    def with_preference_param(self) -> Self: ...
    def _get_user_agent(self) -> str: ...
    def _get_user_hash(self) -> str | None: ...

class PrefixedIndexList(list[str]):
    pass

class PrefixedSearchMixin:
    _original_index: str | list[str]

    def prefix_index(
        self, index: str | list[str] | tuple[str, ...]
    ) -> str | list[str]: ...
    def _clone(self) -> Self: ...

class BaseRecordsSearchV2(dsl.Search):
    def __init__(
        self,
        fields: tuple[str, ...] = ("*",),
        default_filter: Any | None = None,
        **kwargs: Any,
    ) -> None: ...
    def get_record(self, id_: Any) -> Self: ...
    def get_records(self, ids: Iterable[Any]) -> Self: ...
    def with_preference_param(self, preference: str | None = ...) -> Self: ...

class RecordsSearch(PrefixedSearchMixin, BaseRecordsSearch):
    _index: PrefixedIndexList

    def __init__(self, **kwargs: Any) -> None: ...

class Aggs[T]:
    def bucket(self, *args: Any) -> T: ...

class RecordsSearchV2(PrefixedSearchMixin, BaseRecordsSearchV2):
    aggs: Aggs[Self]
    _index: PrefixedIndexList

    def __init__(self, **kwargs: Any) -> None: ...

UnPrefixedRecordsSearch = BaseRecordsSearch
UnPrefixedRecordsSearchV2 = BaseRecordsSearchV2
