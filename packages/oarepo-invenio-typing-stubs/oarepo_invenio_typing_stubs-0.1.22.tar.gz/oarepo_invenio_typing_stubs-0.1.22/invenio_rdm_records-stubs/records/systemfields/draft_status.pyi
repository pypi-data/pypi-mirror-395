from __future__ import annotations

from typing import Any

from invenio_records.systemfields import SystemField

class DraftStatus(SystemField):
    review_to_draft_statuses: dict[str, str]

    def __init__(self, draft_cls: Any | None = ..., key: str | None = ...) -> None: ...
    def __get__(self, record, owner=None): ...
