from typing import ClassVar

from invenio_requests.customizations import RequestType

class ReviewRequest(RequestType):
    """Base class for all review requests."""

    block_publish: ClassVar[bool]
