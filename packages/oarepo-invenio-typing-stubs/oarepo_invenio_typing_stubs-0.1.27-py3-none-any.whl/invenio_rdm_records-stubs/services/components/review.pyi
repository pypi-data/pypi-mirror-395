from typing import Any

from flask_principal import Identity
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.records.api import RDMDraft, RDMRecord

class ReviewComponent(ServiceComponent):
    """Service component for request integration."""

    def create(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMDraft | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def delete_draft(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        force: bool = ...,
    ) -> None: ...
    def publish(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
