from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, ParamSpec, Protocol, TypeAlias

from flask import Response

P = ParamSpec("P")

class SerializerProtocol(Protocol):
    def serialize_object(self, obj: Any) -> str: ...
    def serialize_object_list(self, obj_list: Any) -> str: ...

HeadersFactory = Callable[[Any, int, bool], Mapping[str, str]]

ResponseTuple: TypeAlias = (
    tuple[Any, int]
    | tuple[Any, int, Mapping[str, str]]
    | tuple[Response, int]
    | tuple[Response, int, Mapping[str, str]]
)

def response_handler(
    many: bool = False,
) -> Callable[[Callable[P, Response | ResponseTuple]], Callable[P, Response]]: ...

class ResponseHandler:
    serializer: SerializerProtocol
    headers: Mapping[str, str] | HeadersFactory | None

    def __init__(
        self,
        serializer: SerializerProtocol,
        headers: Mapping[str, str] | HeadersFactory | None = None,
    ) -> None: ...
    def make_headers(
        self,
        obj_or_list: Any,
        code: int,
        many: bool = False,
    ) -> Mapping[str, str]: ...
    def make_response(
        self, obj_or_list: Any, code: int, many: bool = False
    ) -> Response: ...
