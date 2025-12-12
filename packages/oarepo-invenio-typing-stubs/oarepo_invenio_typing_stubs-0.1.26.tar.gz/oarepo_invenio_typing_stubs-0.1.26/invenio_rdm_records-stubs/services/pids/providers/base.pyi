from typing import Any, Optional, Sequence

from flask import Flask
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_rdm_records.records.api import RDMDraft, RDMRecord

class PIDProvider:
    """Base class for PID providers."""

    name: str
    label: str
    client: Any | None
    pid_type: str | None
    default_status: PIDStatus
    managed: bool

    def __init__(
        self,
        name: str,
        client: Any | None = ...,
        pid_type: Optional[str] = ...,
        default_status: PIDStatus = ...,
        managed: bool = ...,
        label: Optional[str] = ...,
        *kwargs: Any,
    ) -> None: ...
    def generate_id(
        self, record: RDMRecord | RDMDraft | dict[str, Any], **kwargs: Any
    ) -> str: ...
    @classmethod
    def is_enabled(cls, app: Flask | None = ...) -> bool: ...
    def is_managed(self) -> bool: ...
    def can_modify(self, pid: PersistentIdentifier, **kwargs: Any) -> bool: ...
    def get(
        self, pid_value: str | int, pid_provider: Optional[str] = ...
    ) -> PersistentIdentifier: ...
    def create(
        self,
        record: Any,
        pid_value: Optional[str] = ...,
        status: Optional[PIDStatus] = ...,
        **kwargs: Any,
    ) -> PersistentIdentifier: ...
    def reserve(
        self,
        pid: PersistentIdentifier,
        record: RDMRecord | RDMDraft | dict[str, Any] | None = ...,
        **kwargs: Any,
    ) -> bool: ...
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
    ) -> bool | None: ...
    def restore(self, pid: PersistentIdentifier, **kwargs: Any) -> None: ...
    def delete(
        self,
        pid: PersistentIdentifier,
        soft_delete: bool = ...,
        **kwargs: Any,
    ) -> Optional[bool]: ...
    def validate(
        self,
        record: RDMRecord | RDMDraft | dict[str, Any],
        identifier: Optional[str] = ...,
        provider: Optional[str] = ...,
        **kwargs: Any,
    ) -> tuple[bool, list[dict[str, Any]]]: ...
    def _insert_pid_type_error_msg(
        self, errors: list[dict[str, Any]], error_msg: str | Sequence[str]
    ) -> None: ...
    def validate_restriction_level(
        self,
        record: RDMRecord | RDMDraft | dict[str, Any],
        identifier: Optional[str],
        **kwargs: Any,
    ) -> None: ...
    def create_and_reserve(
        self, record: RDMRecord | RDMDraft | dict[str, Any], **kwargs: Any
    ) -> None: ...
