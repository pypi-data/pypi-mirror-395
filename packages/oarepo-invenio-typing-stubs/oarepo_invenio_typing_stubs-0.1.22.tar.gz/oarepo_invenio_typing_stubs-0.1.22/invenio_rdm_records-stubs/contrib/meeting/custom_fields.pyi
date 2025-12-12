from typing import Any

from invenio_records_resources.services.custom_fields import BaseCF

class MeetingCF(BaseCF):
    @property
    def field(self): ...
    @property
    def mapping(self) -> dict[str, Any]: ...

MEETING_NAMESPACE: dict[str, str | None]

MEETING_CUSTOM_FIELDS: list[MeetingCF]

MEETING_CUSTOM_FIELDS_UI: dict[str, Any]
