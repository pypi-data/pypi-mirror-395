from __future__ import annotations

from typing import Any

class RequestBodyParser:
    deserializer: Any

    def __init__(self, deserializer: Any) -> None: ...
    def parse(self) -> Any: ...

__all__ = ("RequestBodyParser",)
