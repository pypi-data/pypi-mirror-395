from __future__ import annotations

from typing import Any

from flask_principal import Identity

class StatsPermissionTranslator:
    def __init__(
        self, action_name: str, service: Any | None = ..., **params: Any
    ) -> None: ...
    def translate_params(self, identity: Identity) -> dict[str, Any]: ...
    def can(self) -> bool: ...

def permissions_policy_lookup_factory(
    query_name: str, params: dict[str, Any]
) -> StatsPermissionTranslator | Any: ...
