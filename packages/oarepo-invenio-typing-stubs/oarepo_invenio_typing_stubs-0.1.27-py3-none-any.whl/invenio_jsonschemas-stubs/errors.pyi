from __future__ import annotations

from typing import Any

class JSONSchemaError(Exception): ...

class JSONSchemaNotFound(JSONSchemaError):
    schema: str

    def __init__(self, schema: str, *args: Any, **kwargs: Any) -> None: ...

class JSONSchemaDuplicate(JSONSchemaError):
    schema: str

    def __init__(
        self,
        schema: str,
        first_dir: str,
        second_dir: str,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...
