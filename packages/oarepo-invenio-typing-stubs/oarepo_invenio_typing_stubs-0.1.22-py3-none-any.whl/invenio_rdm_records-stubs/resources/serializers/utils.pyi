from __future__ import annotations

from typing import Any, Iterable, Mapping

def get_vocabulary_props(
    vocabulary: str, fields: Iterable[str], id_: str
) -> Mapping[str, Any]: ...
def get_preferred_identifier(
    priority: Iterable[str], identifiers: list[dict[str, Any]]
) -> dict[str, Any] | None: ...
def convert_size(size_bytes: int) -> str: ...
