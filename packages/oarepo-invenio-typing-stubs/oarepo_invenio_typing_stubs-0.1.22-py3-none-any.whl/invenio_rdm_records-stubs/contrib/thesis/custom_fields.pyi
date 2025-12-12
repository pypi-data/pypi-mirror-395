from typing import Any

from invenio_records_resources.services.custom_fields import BaseCF

class ThesisCF(BaseCF):
    @property
    def field(self): ...
    @property
    def mapping(self) -> dict[str, Any]: ...

THESIS_NAMESPACE: dict[str, str | None]

THESIS_CUSTOM_FIELDS: list[ThesisCF]

THESIS_CUSTOM_FIELDS_UI: dict[str, Any]
