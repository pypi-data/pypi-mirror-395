from __future__ import annotations

from typing import Any

import marshmallow as ma

class RequestParser:
    _location: str
    _unknown: Any
    _schema: type[ma.Schema]

    def __init__(
        self,
        schema_or_dict: type[ma.Schema] | dict[str, Any],
        location: str,
        unknown: Any = ma.EXCLUDE,
    ) -> None: ...
    @property
    def location(self) -> str: ...
    @property
    def default_schema_cls(self) -> type[ma.Schema]: ...
    def schema_from_dict(self, schema_dict: dict[str, Any]) -> type[ma.Schema]: ...
    @property
    def schema(self) -> ma.Schema: ...
    def load_data(self) -> Any: ...
    def parse(self) -> Any: ...

__all__ = ("RequestParser",)
