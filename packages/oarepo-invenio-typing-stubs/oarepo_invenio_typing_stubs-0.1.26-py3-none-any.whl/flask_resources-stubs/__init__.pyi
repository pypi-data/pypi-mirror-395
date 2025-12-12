from __future__ import annotations

from flask_resources.config import from_conf
from flask_resources.content_negotiation import with_content_negotiation
from flask_resources.context import resource_requestctx
from flask_resources.deserializers.json import JSONDeserializer
from flask_resources.errors import HTTPJSONException, create_error_handler
from flask_resources.parsers import (
    BaseListSchema,
    BaseObjectSchema,
    MultiDictSchema,
    RequestBodyParser,
    RequestParser,
    request_body_parser,
    request_parser,
)
from flask_resources.resources import Resource, ResourceConfig, route
from flask_resources.responses import ResponseHandler, response_handler
from flask_resources.serializers import (
    CSVSerializer,
    JSONSerializer,
    MarshmallowSerializer,
)

__version__ = "1.2.0"

__all__: tuple[str, ...] = (
    "__version__",
    "create_error_handler",
    "from_conf",
    "HTTPJSONException",
    "JSONDeserializer",
    "JSONSerializer",
    "CSVSerializer",
    "MultiDictSchema",
    "request_body_parser",
    "request_parser",
    "RequestBodyParser",
    "RequestParser",
    "resource_requestctx",
    "Resource",
    "ResourceConfig",
    "response_handler",
    "ResponseHandler",
    "route",
    "with_content_negotiation",
    "BaseListSchema",
    "MarshmallowSerializer",
    "BaseObjectSchema",
)
