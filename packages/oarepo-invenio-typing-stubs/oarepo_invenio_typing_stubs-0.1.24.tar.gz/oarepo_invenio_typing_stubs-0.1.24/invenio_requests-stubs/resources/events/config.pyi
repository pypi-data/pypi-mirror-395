from collections.abc import Mapping
from typing import Any

from flask_resources.responses import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

class RequestCommentsResourceConfig(RecordResourceConfig):
    # NOTE: configs expose immutable defaults so subclasses override values
    # without mutating shared state.
    blueprint_name: str | None = None
    url_prefix: str | None
    routes: Mapping[str, str]
    request_list_view_args: Mapping[str, Any]
    request_item_view_args: Mapping[str, Any]
    response_handlers: Mapping[str, ResponseHandler]
