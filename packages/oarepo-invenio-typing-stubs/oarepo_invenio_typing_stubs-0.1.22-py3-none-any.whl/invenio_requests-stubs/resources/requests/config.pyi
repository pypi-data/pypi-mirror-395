from collections.abc import Callable, Mapping
from typing import Any

from flask import Response
from flask_resources.responses import ResponseHandler
from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_requests.errors import CannotExecuteActionError as CannotExecuteActionError
from invenio_requests.errors import NoSuchActionError as NoSuchActionError
from invenio_requests.resources.requests.fields import (
    ReferenceString as ReferenceString,
)
from marshmallow import fields
from werkzeug.exceptions import HTTPException

class RequestSearchRequestArgsSchema(SearchRequestArgsSchema):
    created_by: ReferenceString
    topic: ReferenceString
    receiver: ReferenceString
    is_open: fields.Boolean
    shared_with_me: fields.Boolean

request_error_handlers: Mapping[type, Any]

class RequestsResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    # Do not redeclare blueprint_name to avoid incompatible narrowing (base is None)
    # NOTE: configs expose immutable defaults so overrides replace the values
    # rather than mutating shared state.
    url_prefix: str | None
    routes: Mapping[str, str]
    request_view_args: Mapping[str, fields.Field]
    request_search_args: type[SearchRequestArgsSchema]
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]
    response_handlers: Mapping[str, ResponseHandler]
