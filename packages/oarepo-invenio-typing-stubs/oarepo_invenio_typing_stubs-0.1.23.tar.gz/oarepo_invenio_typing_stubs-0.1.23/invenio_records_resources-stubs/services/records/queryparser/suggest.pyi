from __future__ import annotations

from functools import partial
from typing import Any

from invenio_records_resources.services.records.queryparser.query import QueryParser

class SuggestQueryParser(QueryParser):
    """Query parser is useful for search-as-you-type/auto completion features."""

    def __init__(
        self,
        identity: Any | None = None,
        extra_params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None: ...
    def parse(self, query_str: str) -> Any: ...

class CompositeSuggestQueryParser(QueryParser):
    """Composite query parser for suggestion-style queries."""

    filter_field: str | None
    clauses: list[dict[str, Any]]

    def __init__(
        self,
        identity: Any | None = None,
        extra_params: dict[str, Any] | None = None,
        clauses: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> None: ...
    @classmethod
    def factory(  # type: ignore[override]
        cls,
        tree_transformer_cls: type[Any] | None = None,
        clauses: list[dict[str, Any]] | None = None,
        filter_field: str | None = None,
        **extra_params: Any,
    ) -> partial[CompositeSuggestQueryParser]: ...
    def parse(self, query_str: str) -> Any: ...
    def extract_subtypes(self, query_str: str) -> tuple[list[str], str]: ...
