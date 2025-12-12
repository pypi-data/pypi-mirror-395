from typing import Any

from invenio_records_resources.services.custom_fields import BaseCF

class JournalCF(BaseCF):
    @property
    def field(self): ...
    @property
    def mapping(self) -> dict[str, Any]: ...

JOURNAL_NAMESPACE: dict[str, str | None]

JOURNAL_CUSTOM_FIELDS: list[JournalCF]

JOURNAL_CUSTOM_FIELDS_UI: dict[str, Any]
