from typing import Any, Callable, ClassVar

from flask_principal import Identity

class AuditLogAction:
    """Audit log builder for audit operations."""

    context: ClassVar[list[Callable[[dict[str, Any]], Any]]]
    id: ClassVar[str | None]
    resource_type: ClassVar[str | None]
    message_template: ClassVar[str | None]

    @classmethod
    def build(
        cls, identity: Identity, resource_id: Any, **kwargs: Any
    ) -> dict[str, Any] | None: ...
    def resolve_context(self, data: dict[str, Any], **kwargs: Any) -> None: ...
    def render_message(self, data: dict[str, Any]) -> str | None: ...
