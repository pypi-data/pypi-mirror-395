from __future__ import annotations

from invenio_records_resources.records.systemfields.calculated import CalculatedField

class IsVerifiedField(CalculatedField):
    def __init__(self, key: str | None = ...) -> None: ...
    def calculate(self, record) -> bool: ...
