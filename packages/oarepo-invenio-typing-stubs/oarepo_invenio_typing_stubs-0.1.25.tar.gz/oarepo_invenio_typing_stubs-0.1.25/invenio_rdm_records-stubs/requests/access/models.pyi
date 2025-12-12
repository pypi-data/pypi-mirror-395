from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar

class _Model: ...  # keep typing base for SQLAlchemy models

class AccessRequestToken(_Model):
    __tablename__: ClassVar[str]

    id: Any  # UUIDType column
    token: str
    created: datetime
    expires_at: datetime
    email: str
    full_name: str
    message: str
    record_pid: str
    consent_to_share_personal_data: Any

    def delete(self) -> None: ...
    def to_dict(self) -> dict[str, Any]: ...
    @property
    def need(self) -> Any: ...
    @property
    def is_expired(self) -> bool: ...
    @classmethod
    def get_by_token(cls, token: str) -> AccessRequestToken | None: ...
    @classmethod
    def create(
        cls,
        email: str,
        full_name: str,
        message: str,
        record_pid: str,
        shelf_life: Any | None = ...,
        expires_at: datetime | None = ...,
        consent: bool = ...,
    ) -> AccessRequestToken: ...
