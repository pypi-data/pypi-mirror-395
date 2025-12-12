from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any, ClassVar

from flask import Response
from werkzeug.exceptions import HTTPException

class HTTPJSONException(HTTPException):
    errors: ClassVar[Sequence[Mapping[str, Any]] | None]

    def __init__(
        self,
        code: int | None = ...,
        errors: Sequence[Mapping[str, Any]] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    @property
    def name(self) -> str: ...
    def get_errors(self) -> list[Mapping[str, Any]] | None: ...
    def get_description(
        self, environ: Any | None = ..., scope: Mapping[str, Any] | None = ...
    ) -> str: ...
    def get_headers(
        self, environ: Any | None = ..., scope: Mapping[str, Any] | None = ...
    ) -> list[tuple[str, str]]: ...
    def get_body(
        self, environ: Any | None = ..., scope: Mapping[str, Any] | None = ...
    ) -> str: ...

class MIMETypeException(HTTPJSONException):
    header_name: ClassVar[str | None]
    allowed_mimetypes: Sequence[str] | None

    def __init__(
        self, allowed_mimetypes: Sequence[str] | None = ..., **kwargs: Any
    ) -> None: ...

class MIMETypeNotAccepted(MIMETypeException):
    header_name: ClassVar[str | None]

class InvalidContentType(MIMETypeException):
    header_name: ClassVar[str | None]

def create_error_handler(
    map_func_or_exception: Callable[[Exception], HTTPJSONException] | HTTPJSONException,
) -> Callable[[Exception], Response]: ...
def handle_http_exception(exc: HTTPException) -> Response: ...
