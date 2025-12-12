from collections.abc import Callable, Mapping
from typing import Any

import marshmallow as ma
from flask import Response
from flask_resources import ResponseHandler
from invenio_communities.communities.resources.args import (
    CommunitiesSearchRequestArgsSchema as CommunitiesSearchRequestArgsSchema,
)
from invenio_communities.communities.resources.serializer import (
    UICommunityJSONSerializer as UICommunityJSONSerializer,
)
from invenio_communities.errors import CommunityDeletedError as CommunityDeletedError
from invenio_communities.errors import (
    CommunityFeaturedEntryDoesNotExistError as CommunityFeaturedEntryDoesNotExistError,
)
from invenio_communities.errors import LogoNotFoundError as LogoNotFoundError
from invenio_communities.errors import LogoSizeLimitError as LogoSizeLimitError
from invenio_communities.errors import (
    OpenRequestsForCommunityDeletionError as OpenRequestsForCommunityDeletionError,
)
from invenio_communities.errors import (
    SetDefaultCommunityError as SetDefaultCommunityError,
)
from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_requests.resources.requests.config import RequestSearchRequestArgsSchema
from werkzeug.exceptions import HTTPException

community_error_handlers: Mapping[type, Any]

class CommunityResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    # NOTE: configs expose immutable defaults so overrides replace instead of
    # mutating shared state.
    url_prefix: str | None
    routes: Mapping[str, str]
    request_search_args: type[SearchRequestArgsSchema]
    request_view_args: Mapping[str, ma.fields.Field]
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]
    request_community_requests_search_args: type[RequestSearchRequestArgsSchema]
    response_handlers: Mapping[str, ResponseHandler]
