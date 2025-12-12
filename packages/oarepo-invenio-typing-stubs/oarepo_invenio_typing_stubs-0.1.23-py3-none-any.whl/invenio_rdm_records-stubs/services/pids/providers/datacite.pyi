from typing import Any, Optional

from datacite import DataCiteRESTClient
from flask import Flask
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_rdm_records.records.api import RDMDraft, RDMRecord
from invenio_rdm_records.resources.serializers.datacite import DataCite43JSONSerializer

from .base import PIDProvider

class DataCiteClient:
    name: str
    _config_prefix: str
    _config_overrides: dict[str, Any]
    _api: DataCiteRESTClient | None

    def __init__(
        self,
        name: str,
        config_prefix: Optional[str] = ...,
        config_overrides: Optional[dict[str, Any]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def cfgkey(self, key: str) -> str: ...
    def cfg(self, key: str, default: Any | None = ...) -> Any: ...
    def generate_doi(self, record: RDMRecord | RDMDraft | dict[str, Any]) -> str: ...
    def check_credentials(self, **kwargs: Any) -> None: ...
    @property
    def api(self) -> DataCiteRESTClient: ...

class DataCitePIDProvider(PIDProvider):
    serializer: DataCite43JSONSerializer

    def __init__(
        self,
        id_: str,
        client: Optional[DataCiteClient] = ...,
        serializer: Optional[DataCite43JSONSerializer] = ...,
        pid_type: str = ...,
        default_status: PIDStatus = ...,
        **kwargs: Any,
    ) -> None: ...
    @staticmethod
    def _log_errors(exception: Exception) -> None: ...
    def generate_id(self, record: Any, **kwargs: Any) -> str: ...
    @classmethod
    def is_enabled(cls, app: Flask | None = ...) -> bool: ...
    def can_modify(self, pid: PersistentIdentifier, **kwargs: Any) -> bool: ...
    def register(
        self,
        pid: PersistentIdentifier,
        record: RDMRecord | RDMDraft | dict[str, Any] | None = ...,
        **kwargs: Any,
    ) -> bool: ...
    def update(
        self,
        pid: PersistentIdentifier,
        record: RDMRecord | RDMDraft | dict[str, Any] | None = ...,
        url: Optional[str] = ...,
        **kwargs: Any,
    ) -> bool: ...
    def restore(self, pid: PersistentIdentifier, **kwargs: Any) -> None: ...
    def delete(
        self, pid: PersistentIdentifier, soft_delete: bool = ..., **kwargs: Any
    ) -> bool: ...
    def validate(
        self,
        record: RDMRecord | RDMDraft | dict[str, Any],
        identifier: Optional[str] = ...,
        provider: Optional[str] = ...,
        **kwargs: Any,
    ) -> tuple[bool, list[dict[str, Any]]]: ...
    def validate_restriction_level(
        self,
        record: RDMRecord | RDMDraft | dict[str, Any],
        identifier: Optional[str] = ...,
        **kwargs: Any,
    ) -> None: ...
    def create_and_reserve(
        self, record: RDMRecord | RDMDraft | dict[str, Any], **kwargs: Any
    ) -> None: ...
