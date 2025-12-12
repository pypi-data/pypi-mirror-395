from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from typing import Any, Generic, TypeVar

import marshmallow as ma
from flask import Response
from flask_resources import Resource, ResourceConfig, ResponseHandler
from invenio_rdm_records.services.iiif.service import IIIFService
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.resource import (
    request_headers as request_headers,
)
from invenio_records_resources.resources.records.resource import (
    request_read_args as request_read_args,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin
from werkzeug.exceptions import HTTPException
from werkzeug.utils import cached_property

class IIIFResourceConfig(ResourceConfig, ConfiguratorMixin):
    # NOTE: annotate with immutable-friendly defaults so overrides replace them
    # rather than mutating shared state.
    blueprint_name: str | None
    url_prefix: str | None
    routes: Mapping[str, str]
    request_view_args: Mapping[str, ma.fields.Field]
    request_read_args: Mapping[str, ma.fields.Field]
    request_headers: Mapping[str, ma.fields.Field]
    response_handler: Mapping[str, ResponseHandler]
    supported_formats: Any
    proxy_cls: Any
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]

def with_iiif_content_negotiation(
    serializer: type,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...

iiif_request_view_args: Any

C = TypeVar("C", bound=IIIFResourceConfig)
S = TypeVar("S", bound=IIIFService)

class IIIFResource(ErrorHandlersMixin, Resource[C], Generic[C, S]):
    service: S
    def __init__(self, config: C, service: S) -> None: ...
    @cached_property
    def proxy(self) -> Callable[[], Any] | None: ...
    @staticmethod
    def proxy_pass(f: Callable[..., Any]) -> Callable[..., Any]: ...
    def create_url_rules(self) -> list[Any]: ...
    def _get_record_with_files(self) -> Any: ...
    def manifest(self) -> tuple[dict[str, Any], int]: ...
    def sequence(self) -> tuple[dict[str, Any], int]: ...
    def canvas(self) -> tuple[dict[str, Any], int]: ...
    def base(self) -> Any: ...
    def info(self) -> tuple[dict[str, Any], int]: ...
    def image_api(self) -> Response: ...

class IIIFProxy(ABC):
    def should_proxy(self) -> bool: ...
    @abstractmethod
    def proxy_request(self) -> Any: ...
    def __call__(self) -> Any: ...

class IIPServerProxy(IIIFProxy):
    @property
    def server_url(self) -> str | None: ...
    def proxy_request(self) -> Response | None: ...
    def _rewrite_url(self) -> str: ...
