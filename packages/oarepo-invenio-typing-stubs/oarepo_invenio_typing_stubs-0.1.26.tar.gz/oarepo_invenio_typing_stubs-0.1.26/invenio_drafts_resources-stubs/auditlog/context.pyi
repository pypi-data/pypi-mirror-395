from typing import Any

from invenio_users_resources.entity_resolvers import UserResolver

class UserContext:
    key: str
    resolver: UserResolver
    def __init__(self, key: str = "user") -> None: ...
    def __call__(
        self, data: dict[str, Any], lookup_key: str = "user_id", **kwargs: Any
    ) -> None: ...

class RecordContext:
    def __call__(self, data: dict[str, Any], **kwargs: Any) -> None: ...

class RequestContext:
    def __call__(self, data: dict[str, Any], **kwargs: Any) -> None: ...
