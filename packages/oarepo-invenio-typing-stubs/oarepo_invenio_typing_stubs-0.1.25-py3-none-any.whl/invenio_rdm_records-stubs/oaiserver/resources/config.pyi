from collections.abc import Callable, Mapping
from typing import Any

import marshmallow as ma
from flask import Response
from flask_resources import ResourceConfig
from flask_resources.responses import ResponseHandler
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema
from invenio_records_resources.services.base.config import ConfiguratorMixin
from werkzeug.exceptions import HTTPException

oaipmh_error_handlers: Mapping[
    int | type[HTTPException] | type[BaseException],
    Callable[[Exception], Response],
]

class OAIPMHServerSearchRequestArgsSchema(SearchRequestArgsSchema):
    managed: ma.fields.Boolean
    sort_direction: ma.fields.Str

class OAIPMHServerResourceConfig(ResourceConfig, ConfiguratorMixin):
    # NOTE: configs expose immutable defaults so overrides replace them instead
    # of mutating shared state.
    blueprint_name: str | None
    url_prefix: str | None
    routes: Mapping[str, str]

    request_read_args: Mapping[str, Any]
    request_view_args: Mapping[str, ma.fields.Field]
    request_search_args: (
        type[SearchRequestArgsSchema] | type[OAIPMHServerSearchRequestArgsSchema]
    )

    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]

    response_handlers: Mapping[str, ResponseHandler]
