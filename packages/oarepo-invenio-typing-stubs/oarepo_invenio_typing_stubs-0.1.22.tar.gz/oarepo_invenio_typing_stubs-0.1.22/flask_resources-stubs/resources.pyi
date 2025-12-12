from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, ClassVar, Generic, TypeVar

from flask import Blueprint, Response
from flask_resources.config import ConfigAttrValue
from flask_resources.parsers import RequestBodyParser
from flask_resources.responses import ResponseHandler, ResponseTuple
from werkzeug.exceptions import HTTPException

ViewCallable = Callable[..., Response | ResponseTuple]
Decorator = Callable[[ViewCallable], ViewCallable]

def route(
    method: str,
    rule: str | ConfigAttrValue[Any],
    view_meth: ViewCallable,
    endpoint: str | None = ...,
    rule_options: Mapping[str, Any] | None = ...,
    apply_decorators: bool = ...,
) -> dict[str, Any]: ...

class ResourceConfig:
    # NOTE: configs now expose immutable-friendly defaults so they can be
    # overridden per-instance without mutating shared class state.
    blueprint_name: str | None
    url_prefix: str | None
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]
    request_body_parsers: Mapping[str, RequestBodyParser]
    default_content_type: str | None
    response_handlers: Mapping[str, ResponseHandler]
    default_accept_mimetype: str | None

C = TypeVar("C", bound=ResourceConfig)

class Resource(Generic[C]):
    config: C
    decorators: ClassVar[Sequence[Decorator]]
    error_handlers: ClassVar[
        dict[
            int | type[HTTPException] | type[BaseException],
            Callable[[Exception], Response],
        ]
    ]

    def __init__(self, config: ResourceConfig) -> None: ...
    def as_blueprint(self, **options: Any) -> Blueprint: ...
    def create_blueprint(self, **options: Any) -> Blueprint: ...
    def create_url_rules(self) -> Sequence[dict[str, Any]]: ...
    def create_error_handlers(
        self,
    ) -> Iterable[
        tuple[
            int | type[HTTPException] | type[BaseException],
            Callable[[Exception], Response],
        ]
    ]: ...
