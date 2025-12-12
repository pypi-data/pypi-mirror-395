from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, ParamSpec, TypeVar

import marshmallow as ma
from flask_resources.config import ConfigAttrValue
from flask_resources.parsers.base import RequestParser
from flask_resources.parsers.body import RequestBodyParser

P = ParamSpec("P")
R = TypeVar("R")

ParsersMapping = (
    Mapping[str, RequestBodyParser]
    | dict[str, RequestBodyParser]
    | ConfigAttrValue[Mapping[str, RequestBodyParser]]
)

def request_parser(
    schema_or_parser: (
        ConfigAttrValue[RequestParser | type[ma.Schema] | dict[str, Any]]
        | RequestParser
        | type[ma.Schema]
        | dict[str, Any]
    ),
    location: str | None = ...,
    **options: Any,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
def request_body_parser(
    parsers: ParsersMapping = ...,
    default_content_type: str | ConfigAttrValue[str | None] | None = ...,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

__all__ = ("request_parser", "request_body_parser")
