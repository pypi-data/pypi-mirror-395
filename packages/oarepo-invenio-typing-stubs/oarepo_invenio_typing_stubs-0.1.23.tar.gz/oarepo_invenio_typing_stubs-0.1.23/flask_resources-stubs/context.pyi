from __future__ import annotations

from collections.abc import Callable, Mapping
from types import TracebackType
from typing import Any, Protocol

from flask import Response

class ResponseHandlerProtocol(Protocol):
    def make_response(
        self, obj_or_list: Any, code: int, many: bool = False
    ) -> Response: ...

class ResourceConfigProtocol(Protocol):
    blueprint_name: str | None
    url_prefix: str | None
    error_handlers: Mapping[Any, Callable[[Exception], Response]]
    request_body_parsers: Mapping[str, Any]
    default_content_type: str | None
    response_handlers: Mapping[str, ResponseHandlerProtocol]
    default_accept_mimetype: str | None

class ResourceRequestCtx:
    config: ResourceConfigProtocol
    args: Mapping[str, Any]  # intentionally not None as it is initialized to {}
    headers: Mapping[str, str]  # intentionally not None as it is initialized to {}
    data: Any
    view_args: Mapping[str, Any]  # intentionally not None as it is initialized to {}
    accept_mimetype: str | None
    response_handler: ResponseHandlerProtocol | None

    def __init__(self, config: ResourceConfigProtocol) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        type: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def update(self, values: Mapping[str, Any]) -> None: ...

def _get_context() -> ResourceRequestCtx: ...

resource_requestctx: ResourceRequestCtx  # intentionally not using a LocalProxy[ResourceRequestCtx] here as mypy does not understand it
