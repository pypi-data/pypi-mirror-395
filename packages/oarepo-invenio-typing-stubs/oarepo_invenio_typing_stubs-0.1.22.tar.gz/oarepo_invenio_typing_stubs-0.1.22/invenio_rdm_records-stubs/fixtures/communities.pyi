from __future__ import annotations

from typing import Any

class CommunitiesFixture:
    def __init__(
        self,
        search_paths: list[Any],
        filename: str,
        create_record_func: Any,
        logo_path: Any | None = ...,
        delay: bool = ...,
    ) -> None: ...
    def create(self, entry: dict[str, Any]) -> None: ...
