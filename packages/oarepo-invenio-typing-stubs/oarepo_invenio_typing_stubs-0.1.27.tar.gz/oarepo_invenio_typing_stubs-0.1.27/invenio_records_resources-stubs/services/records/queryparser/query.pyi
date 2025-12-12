from __future__ import annotations

from functools import partial
from typing import Any

class QueryParser:
    """Parse a query string into a search engine DSL Q object."""

    identity: Any | None
    tree_transformer_cls: type[Any] | None
    extra_params: dict[str, Any]
    mapping: dict[str, str]
    _allow_list: list[str] | None
    _fields: list[str]

    def __init__(
        self,
        identity: Any | None = None,
        extra_params: dict[str, Any] | None = None,
        tree_transformer_cls: type[Any] | None = None,
    ) -> None: ...
    @property
    def allow_list(self) -> set[str]: ...
    @property
    def fields(self) -> list[str]: ...
    @classmethod
    def factory(
        cls,
        tree_transformer_cls: type[Any] | None = None,
        **extra_params: Any,
    ) -> partial[QueryParser]: ...
    def parse(self, query_str: str) -> Any: ...
