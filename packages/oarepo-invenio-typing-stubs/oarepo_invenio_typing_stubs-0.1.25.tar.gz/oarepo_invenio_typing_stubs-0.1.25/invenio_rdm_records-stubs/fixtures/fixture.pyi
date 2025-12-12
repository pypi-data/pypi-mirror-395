from __future__ import annotations

from typing import Any

class FixtureMixin:
    def __init__(
        self,
        search_paths: list[Any],
        filename: str,
        create_record_func: Any | None = ...,
        delay: bool = ...,
    ) -> None: ...
    def load(self) -> None: ...
    def read(self) -> list[Any] | None: ...
    def create_record(self, *args: Any, **kwargs: Any) -> None: ...
