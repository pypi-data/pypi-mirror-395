from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any, ParamSpec, Protocol, TypeAlias, TypeVar

from flask import Response
from flask_resources.config import ConfigAttrValue
from werkzeug.datastructures import MIMEAccept

P = ParamSpec("P")
R = TypeVar("R")

class ResponseHandlerProtocol(Protocol):
    def make_response(
        self, obj_or_list: Any, code: int, many: bool = False
    ) -> Response: ...

ResponseHandlersResolvable: TypeAlias = (
    ConfigAttrValue[Mapping[str, ResponseHandlerProtocol]]
    | Mapping[str, ResponseHandlerProtocol]
    | None
)

class ContentNegotiator:
    @classmethod
    def match(
        cls,
        mimetypes: Iterable[str],
        accept_mimetypes: MIMEAccept,
        formats_map: Mapping[str, str],
        fmt: str | None,
        default: str | None = ...,
    ) -> str | None: ...
    @classmethod
    def match_by_accept(
        cls,
        mimetypes: Iterable[str],
        accept_mimetypes: MIMEAccept,
        default: str | None = ...,
    ) -> str | None: ...
    @classmethod
    def match_by_format(
        cls, formats_map: Mapping[str, str], fmt: str | None
    ) -> str | None: ...

def with_content_negotiation(
    response_handlers: ResponseHandlersResolvable = ...,
    default_accept_mimetype: ConfigAttrValue[str | None] | str | None = ...,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
