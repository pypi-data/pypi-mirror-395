from flask_principal import Identity
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.records.api import RDMDraft, RDMRecord

class RecordFilesProcessorComponent(ServiceComponent):
    """Service component for RecordFilesProcessor."""

    def publish(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
    ) -> None: ...
    def lift_embargo(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
    ) -> None: ...
