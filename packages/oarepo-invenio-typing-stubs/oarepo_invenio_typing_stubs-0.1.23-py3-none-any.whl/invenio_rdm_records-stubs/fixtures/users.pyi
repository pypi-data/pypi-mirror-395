from __future__ import annotations

from typing import Any

class UsersFixture:
    def _get_password(self, email: str, entry: dict[str, Any]) -> str: ...
    def create(self, entry: dict[str, Any]) -> None: ...
