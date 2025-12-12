from typing import Any

from flask_principal import Identity
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.records.api import RDMDraft, RDMRecord

class MetadataComponent(ServiceComponent):
    field: str
    new_version_skip_fields: list[str]
    def create(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMDraft | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def update_draft(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMDraft | None = ...,
        errors: Any | None = ...,
    ) -> None: ...
    def publish(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def edit(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def new_version(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
