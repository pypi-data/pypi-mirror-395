from __future__ import annotations

from datetime import date, datetime
from typing import Any

from flask_principal import Need

SUPPORTED_DIGEST_ALGORITHMS: tuple[str, ...]

class _Model: ...  # keep typing base for SQLAlchemy models

class SecretLink(_Model):
    id: Any
    token: str
    created: datetime
    expires_at: datetime | None
    permission_level: str
    origin: str
    description: str

    def revoke(self) -> None: ...
    def to_dict(self) -> dict[str, Any]: ...
    @property
    def need(self) -> Need: ...
    @property
    def extra_data(self) -> dict[str, Any] | None: ...
    @property
    def is_expired(self) -> bool: ...
    @classmethod
    def get_by_token(cls, token: str) -> SecretLink | None: ...
    @classmethod
    def create(
        cls,
        permission_level: str,
        extra_data: dict[str, Any] | None = ...,
        expires_at: date | datetime | None = ...,
        origin: str | None = ...,
        description: str | None = ...,
    ) -> SecretLink: ...
    @classmethod
    def validate_token(cls, token: str, expected_data: dict[str, Any]) -> bool: ...
    @staticmethod
    def load_token(
        token: str, expected_data: dict[str, Any] | None = ..., *, force: bool = ...
    ) -> dict[str, Any] | None: ...
