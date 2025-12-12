from collections.abc import Callable, Mapping
from typing import Any

import marshmallow as ma
from flask import Response
from flask_resources import RequestBodyParser, ResourceConfig, ResponseHandler
from invenio_communities.communities.resources.args import (
    CommunitiesSearchRequestArgsSchema as CommunitiesSearchRequestArgsSchema,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin
from werkzeug.exceptions import HTTPException

json_response_handler: ResponseHandler

class SubCommunityResourceConfig(ConfiguratorMixin, ResourceConfig):
    # NOTE: annotate with immutable-friendly defaults to prevent shared mutable
    # state while still allowing subclass overrides.
    blueprint_name: str | None
    url_prefix: str | None
    routes: Mapping[str, str]
    request_view_args: Mapping[str, ma.fields.Field]
    request_read_args: Mapping[str, Any]
    request_extra_args: Mapping[str, ma.fields.Field]
    request_body_parsers: Mapping[str, RequestBodyParser]
    default_content_type: str | None
    request_search_args: type[CommunitiesSearchRequestArgsSchema]
    response_handlers: Mapping[str, ResponseHandler]
    default_accept_mimetype: str | None
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]
