from invenio_requests.resources.events import (
    RequestCommentsResource as RequestCommentsResource,
)
from invenio_requests.resources.events import (
    RequestCommentsResourceConfig as RequestCommentsResourceConfig,
)
from invenio_requests.resources.requests import RequestsResource as RequestsResource
from invenio_requests.resources.requests import (
    RequestsResourceConfig as RequestsResourceConfig,
)

__all__ = [
    "RequestsResource",
    "RequestsResourceConfig",
    "RequestCommentsResource",
    "RequestCommentsResourceConfig",
]
