from typing import Any, Mapping, Optional

from marshmallow import fields

class UIAccessStatus:
    """Access status properties to display in the UI."""

    def __init__(self, access_status: str) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def title(self) -> str: ...
    @property
    def icon(self) -> str: ...

class UIObjectAccessStatus(UIAccessStatus):
    """Record or draft access status UI properties."""

    def __init__(
        self, record_access_dict: Mapping[str, Any], has_files: bool
    ) -> None: ...
    @property
    def description(self) -> str: ...
    @property
    def embargo_date(self) -> Optional[str]: ...
    @property
    def message_class(self) -> str: ...

class AccessStatusField(fields.Field):
    """Record access status."""

    def _serialize(
        self, value: Any, attr: Optional[str], obj: Any, **kwargs: Any
    ) -> Optional[Mapping[str, Any]]: ...
