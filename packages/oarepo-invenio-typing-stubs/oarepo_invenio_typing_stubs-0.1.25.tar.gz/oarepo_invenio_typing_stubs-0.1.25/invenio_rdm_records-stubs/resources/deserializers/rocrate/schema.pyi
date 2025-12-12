from __future__ import annotations

from typing import Any

from marshmallow import Schema

def _list_value(lst: Any) -> Any: ...

class ROCrateSchema(Schema):
    class Meta:
        unknown: Any

    error_messages: dict[str, Any]
    LIST_VALUE_FIELDS: list[str]

    def list_to_value(self, data: dict[str, Any], **kwargs: Any) -> dict[str, Any]: ...
    def load_publication_date(self, value: Any) -> Any: ...
    def load_creators(self, value: list[dict[str, Any]]) -> list[dict[str, Any]]: ...
    def load_rights(
        self, value: dict[str, Any] | None
    ) -> list[dict[str, Any]] | None: ...
    def load_subjects(self, value: list[str] | None) -> list[dict[str, str]]: ...
