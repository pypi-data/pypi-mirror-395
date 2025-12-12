from typing import Any

from flask_principal import Identity
from invenio_drafts_resources.services.records.components import DraftFilesComponent
from invenio_records_resources.records.api import Record

class RDMDraftFilesComponent(DraftFilesComponent):
    def create(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: Record | None = ...,
        errors: Any | None = ...,
        **kwargs: Any,
    ) -> None: ...
