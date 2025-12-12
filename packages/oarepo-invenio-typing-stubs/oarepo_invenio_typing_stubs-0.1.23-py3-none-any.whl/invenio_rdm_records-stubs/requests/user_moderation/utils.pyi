from __future__ import annotations

from collections.abc import Generator
from typing import Any, Iterable

def get_user_records(
    user_id: str | int, from_db: bool = ..., status: Iterable[Any] | None = ...
) -> Generator[str, None, None]: ...
