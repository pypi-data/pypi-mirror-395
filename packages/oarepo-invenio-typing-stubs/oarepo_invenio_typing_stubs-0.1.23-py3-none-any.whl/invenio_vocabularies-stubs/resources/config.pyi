from collections.abc import Callable, Mapping
from typing import Any

import marshmallow as ma
from flask import Response
from flask_resources import HTTPJSONException as HTTPJSONException
from flask_resources import ResourceConfig
from flask_resources import create_error_handler as create_error_handler
from flask_resources.responses import ResponseHandler
from invenio_records_resources.resources import RecordResource as RecordResource
from invenio_records_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_vocabularies.resources.serializer import (
    VocabularyL10NItemSchema as VocabularyL10NItemSchema,
)
from werkzeug.exceptions import HTTPException

class VocabularySearchRequestArgsSchema(SearchRequestArgsSchema):
    tags: ma.fields.Str
    active: ma.fields.Boolean
    status: ma.fields.Boolean

class VocabulariesResourceConfig(RecordResourceConfig):
    # NOTE: immutable annotations avoid shared mutable defaults between configs.
    blueprint_name: str | None = None
    url_prefix: str | None
    routes: Mapping[str, str]
    request_view_args: Mapping[str, ma.fields.Field]
    request_search_args = VocabularySearchRequestArgsSchema
    response_handlers: Mapping[str, ResponseHandler]

class VocabularyTypeResourceConfig(ResourceConfig, ConfiguratorMixin):
    # NOTE: configs expose immutable defaults to prevent accidental mutation.
    blueprint_name: str | None
    url_prefix: str | None
    routes: Mapping[str, str]
    request_read_args: Mapping[str, Any]
    request_view_args: Mapping[str, ma.fields.Field]
    request_search_args = VocabularySearchRequestArgsSchema
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]
    response_handlers: Mapping[str, ResponseHandler]
