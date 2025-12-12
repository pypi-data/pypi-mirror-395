from typing import Any

from flask_resources import HTTPJSONException as _HTTPJSONException

class HTTPJSONValidationWithMessageAsListException(_HTTPJSONException):
    description: str | None
    def __init__(self, exception) -> None: ...

class HTTPJSONException(_HTTPJSONException):
    def __init__(
        self, code: int | None = ..., errors: Any | None = ..., **kwargs: Any
    ) -> None: ...
    def get_body(self, environ=None, scope=None) -> str: ...
