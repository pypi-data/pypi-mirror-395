from __future__ import annotations

from typing import Any, Mapping

def file_download_event_builder(
    event: dict[str, Any], sender_app: Any, **kwargs: Any
) -> dict[str, Any]: ...
def record_view_event_builder(
    event: dict[str, Any], sender_app: Any, **kwargs: Any
) -> dict[str, Any] | None: ...
def check_if_via_api(
    event: dict[str, Any], sender_app: Any, **kwargs: Any
) -> dict[str, Any]: ...
def drop_if_via_api(
    event: Mapping[str, Any], sender_app: Any, **kwargs: Any
) -> Mapping[str, Any] | None: ...
def build_record_unique_id(event: dict[str, Any]) -> dict[str, Any]: ...
