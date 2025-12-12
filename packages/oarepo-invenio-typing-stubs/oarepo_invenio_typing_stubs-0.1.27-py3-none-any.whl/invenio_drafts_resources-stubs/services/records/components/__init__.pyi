from invenio_drafts_resources.services.records.components.base import (
    ServiceComponent as ServiceComponent,
)
from invenio_drafts_resources.services.records.components.files import (
    DraftFilesComponent as DraftFilesComponent,
)
from invenio_drafts_resources.services.records.components.media_files import (
    DraftMediaFilesComponent as DraftMediaFilesComponent,
)
from invenio_drafts_resources.services.records.components.metadata import (
    DraftMetadataComponent as DraftMetadataComponent,
)
from invenio_drafts_resources.services.records.components.pid import (
    PIDComponent as PIDComponent,
)
from invenio_drafts_resources.services.records.components.relations import (
    RelationsComponent as RelationsComponent,
)

__all__ = [
    "ServiceComponent",
    "DraftFilesComponent",
    "DraftMetadataComponent",
    "PIDComponent",
    "RelationsComponent",
    "DraftMediaFilesComponent",
]
