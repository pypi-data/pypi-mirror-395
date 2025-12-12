from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

class RequestLink: ...  # keep typing: imported from invenio_requests.services.requests.links at runtime

def request_next_link(**kwargs: Any) -> Callable[[F], F]: ...
