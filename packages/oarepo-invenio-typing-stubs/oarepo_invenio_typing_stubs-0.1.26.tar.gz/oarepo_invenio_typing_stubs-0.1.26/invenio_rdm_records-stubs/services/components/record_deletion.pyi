from typing import Any

from flask_principal import Identity
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.records.api import RDMRecord

class RecordDeletionComponent(ServiceComponent):
    """Service component for record deletion."""

    def delete_record(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def update_tombstone(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def restore_record(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def mark_record(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def unmark_record(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
