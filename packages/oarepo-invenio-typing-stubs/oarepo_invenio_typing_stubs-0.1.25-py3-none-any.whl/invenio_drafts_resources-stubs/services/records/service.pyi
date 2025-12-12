from typing import Generic, TypeVar

from flask_principal import Identity
from invenio_drafts_resources.auditlog.actions import (
    DraftCreateAuditLog as DraftCreateAuditLog,
)
from invenio_drafts_resources.auditlog.actions import (
    DraftDeleteAuditLog as DraftDeleteAuditLog,
)
from invenio_drafts_resources.auditlog.actions import (
    DraftEditAuditLog as DraftEditAuditLog,
)
from invenio_drafts_resources.auditlog.actions import (
    DraftNewVersionAuditLog as DraftNewVersionAuditLog,
)
from invenio_drafts_resources.auditlog.actions import (
    RecordPublishAuditLog as RecordPublishAuditLog,
)
from invenio_drafts_resources.resources.records.errors import (
    DraftNotCreatedError as DraftNotCreatedError,
)
from invenio_drafts_resources.services.records.config import RecordServiceConfig
from invenio_drafts_resources.services.records.uow import (
    ParentRecordCommitOp as ParentRecordCommitOp,
)
from invenio_records_resources.services import RecordService as RecordServiceBase

C = TypeVar("C", bound=RecordServiceConfig)

class RecordService(RecordServiceBase[C], Generic[C]):
    def __init__(
        self, config, files_service=None, draft_files_service=None
    ) -> None: ...
    @property
    def files(self): ...
    @property
    def draft_files(self): ...
    @property
    def schema_parent(self): ...
    @property
    def draft_cls(self): ...
    @property
    def draft_indexer(self): ...
    def search_drafts(
        self,
        identity: Identity,
        params=None,
        search_preference=None,
        expand: bool = False,
        extra_filter=None,
        **kwargs,
    ): ...
    def search_versions(
        self,
        identity: Identity,
        id_,
        params=None,
        search_preference=None,
        expand: bool = False,
        permission_action: str = "read",
        **kwargs,
    ): ...
    def read_draft(self, identity: Identity, id_, expand: bool = False): ...
    def read_latest(self, identity: Identity, id_, expand: bool = False): ...
    def update_draft(
        self,
        identity: Identity,
        id_,
        data,
        revision_id=None,
        uow=None,
        expand: bool = False,
    ): ...
    def edit(self, identity: Identity, id_, uow=None, expand: bool = False): ...
    def publish(self, identity: Identity, id_, uow=None, expand: bool = False): ...
    def new_version(self, identity: Identity, id_, uow=None, expand: bool = False): ...
    def delete_draft(self, identity: Identity, id_, revision_id=None, uow=None): ...
    def import_files(self, identity: Identity, id_, uow=None): ...
    def validate_draft(
        self, identity: Identity, id_, ignore_field_permissions: bool = False
    ) -> None: ...
    def cleanup_drafts(
        self, timedelta, uow=None, search_gc_deletes: int = 60
    ) -> None: ...
    def reindex_latest_first(
        self, identity: Identity, search_preference=None, extra_filter=None, uow=None
    ): ...
    def rebuild_index(self, identity: Identity) -> bool: ...  # type: ignore[override]
