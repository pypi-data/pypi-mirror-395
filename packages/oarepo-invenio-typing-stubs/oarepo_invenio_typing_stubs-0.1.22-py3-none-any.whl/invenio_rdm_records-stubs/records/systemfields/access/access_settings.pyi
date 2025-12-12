from __future__ import annotations

from typing import Any

class AccessSettings:
    """Access settings for a parent record."""

    allow_user_requests: bool
    allow_guest_requests: bool
    accept_conditions_text: str | None
    secret_link_expiration: int

    def __init__(self, settings_dict: dict[str, Any]) -> None: ...
    def dump(self) -> dict[str, Any]: ...
    def __repr__(self) -> str: ...
