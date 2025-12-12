from __future__ import annotations

from collections.abc import Callable, Generator
from typing import Any

from invenio_access.permissions import Permission  # type: ignore[import-untyped]
from luqum.tree import Phrase, SearchField, Word  # type: ignore[import-untyped]
from luqum.visitor import TreeTransformer  # type: ignore[import-untyped]

class FieldValueMapper:
    """Class used to remap values to new terms."""

    _term_name: str
    _word_fun: Callable[[Any], Any] | None
    _phrase_fun: Callable[[Any], Any] | None

    def __init__(
        self,
        term_name: str,
        word: Callable[[Any], Any] | None = None,
        phrase: Callable[[Any], Any] | None = None,
    ) -> None: ...
    @property
    def term_name(self) -> str: ...
    def map_word(self, node: Word, **kwargs: Any) -> Any: ...
    def map_phrase(self, node: Phrase, **kwargs: Any) -> Any: ...

class RestrictedTerm:
    """Class used to apply specific permissions to search."""

    permission: Permission

    def __init__(self, permission: Permission) -> None: ...
    def allows(self, identity: Any) -> bool: ...

class RestrictedTermValue:
    """Class used to apply specific permissions to search specific words."""

    permission: Permission
    _word_fun: Callable[[Any], Any] | None
    _phrase_fun: Callable[[Any], Any] | None

    def __init__(
        self,
        permission: Permission,
        word: Callable[[Any], Any] | None = None,
        phrase: Callable[[Any], Any] | None = None,
    ) -> None: ...
    def map_word(
        self,
        node: Word,
        context: dict[str, Any],
        **kwargs: Any,
    ) -> Any: ...
    def map_phrase(
        self,
        node: Phrase,
        context: dict[str, Any],
        **kwargs: Any,
    ) -> Any: ...

class SearchFieldTransformer(TreeTransformer):
    """Transform from user-friendly field names to internal field names."""

    _mapping: dict[str, Any]
    _allow_list: set[str]

    def __init__(
        self,
        mapping: dict[str, Any],
        allow_list: set[str],
        *args: Any,
        **kwargs: Any,
    ) -> None: ...
    def visit_search_field(
        self,
        node: SearchField,
        context: dict[str, Any],
    ) -> Generator[SearchField, None, None]: ...
    def visit_word(
        self,
        node: Word,
        context: dict[str, Any],
    ) -> Generator[Word, None, None]: ...
    def visit_phrase(
        self,
        node: Phrase,
        context: dict[str, Any],
    ) -> Generator[Phrase, None, None]: ...
