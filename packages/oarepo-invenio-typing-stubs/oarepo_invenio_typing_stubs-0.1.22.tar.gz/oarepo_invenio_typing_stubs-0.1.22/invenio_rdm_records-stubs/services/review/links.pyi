from __future__ import annotations

from typing import Any

from invenio_records_resources.services.base.links import Link

class RequestRecordLink(Link):
    @staticmethod
    def vars(request: dict[str, Any], vars: dict[str, Any]) -> None: ...
