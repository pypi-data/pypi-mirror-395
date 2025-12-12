from typing import Any

from flask import Flask
from invenio_pidstore.models import PersistentIdentifier
from invenio_rdm_records.records.api import RDMDraft, RDMRecord

from .base import PIDProvider

class OAIPIDProvider(PIDProvider):
    name: str

    def __init__(self, name: str, **kwargs: Any) -> None: ...
    def generate_id(self, record: Any, **kwargs: Any) -> str: ...
    @classmethod
    def is_enabled(cls, app: Flask | None = ...) -> bool: ...
    def reserve(
        self,
        pid: PersistentIdentifier,
        record: RDMRecord | RDMDraft | dict[str, Any] | None = ...,
        **kwargs: Any,
    ) -> bool: ...
