from typing import Any, Mapping, Optional

from invenio_communities.proxies import current_roles as current_roles
from invenio_communities.roles import Role
from marshmallow import fields

class RoleField(fields.Str):
    default_error_messages: dict[str, str]
    roles: Any
    def __init__(self, *args, **kwargs) -> None: ...
    def _deserialize(
        self,
        value: str,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs,
    ) -> Role: ...
    def _serialize(
        self,
        value: Role | str | None,
        attr: Optional[str],
        obj: Any,
        **kwargs,
    ) -> str | None: ...
