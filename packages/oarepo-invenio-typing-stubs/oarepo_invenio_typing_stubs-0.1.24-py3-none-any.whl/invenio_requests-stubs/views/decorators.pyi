from collections.abc import Callable
from typing import Any

from invenio_requests.proxies import current_requests as current_requests

def pass_request(
    expand: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...
