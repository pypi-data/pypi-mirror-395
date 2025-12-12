from __future__ import annotations

from typing import Any

from invenio_db.uow import UnitOfWork

def on_block(
    user_id: str | int, uow: UnitOfWork | None = ..., **kwargs: Any
) -> None: ...
def on_restore(
    user_id: str | int, uow: UnitOfWork | None = ..., **kwargs: Any
) -> None: ...
def on_approve(
    user_id: str | int, uow: UnitOfWork | None = ..., **kwargs: Any
) -> None: ...
