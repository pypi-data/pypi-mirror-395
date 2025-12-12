from typing import Any

from invenio_records_resources.services.custom_fields import BaseCF

class ImprintCF(BaseCF):
    @property
    def field(self): ...
    @property
    def mapping(self) -> dict[str, Any]: ...

IMPRINT_NAMESPACE: dict[str, str | None]

IMPRINT_CUSTOM_FIELDS: list[ImprintCF]

IMPRINT_CUSTOM_FIELDS_UI: dict[str, Any]
