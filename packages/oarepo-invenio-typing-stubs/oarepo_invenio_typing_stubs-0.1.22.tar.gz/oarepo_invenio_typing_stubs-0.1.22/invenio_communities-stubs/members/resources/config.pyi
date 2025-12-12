from collections.abc import Callable, Mapping

import marshmallow as ma
from flask import Response
from flask_resources import ResponseHandler
from invenio_communities.errors import CommunityDeletedError as CommunityDeletedError
from invenio_communities.members.errors import (
    AlreadyMemberError as AlreadyMemberError,
)
from invenio_communities.members.errors import (
    InvalidMemberError as InvalidMemberError,
)
from invenio_records_resources.resources import RecordResourceConfig
from werkzeug.exceptions import HTTPException

class MemberResourceConfig(RecordResourceConfig):
    # NOTE: configs expose immutable defaults so overrides replace values
    # instead of mutating shared state.
    url_prefix: str | None
    routes: Mapping[str, str]
    request_view_args: Mapping[str, ma.fields.Field]
    # Mapping from exception type to an error handler (callable or factory)
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]
    response_handlers: Mapping[str, ResponseHandler]
