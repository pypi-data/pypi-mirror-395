from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

from flask_principal import Identity
from invenio_drafts_resources.services.records.service import RecordService
from invenio_rdm_records.services.config import RDMRecordServiceConfig
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper

C = TypeVar("C", bound=RDMRecordServiceConfig)

class RDMRecordService(RecordService[C], Generic[C]):
    def __init__(
        self,
        config,
        files_service=None,
        draft_files_service=None,
        access_service=None,
        pids_service=None,
        review_service=None,
    ) -> None: ...

    # Subservices
    @property
    def access(self): ...
    @property
    def pids(self): ...
    @property
    def review(self): ...

    # Properties
    @property
    def expandable_fields(self) -> list[Any]: ...
    @property
    def schema_tombstone(self) -> ServiceSchemaWrapper: ...
    @property
    def schema_quota(self) -> ServiceSchemaWrapper: ...

    # Service methods
    def lift_embargo(self, identity: Identity, _id: str, uow=None): ...
    def scan_expired_embargos(self, identity): ...
    def oai_result_item(self, identity: Identity, oai_record_source): ...
    def delete_record(
        self,
        identity: Identity,
        id_: str,
        data,
        expand: bool = ...,
        uow=None,
        revision_id: Optional[int] = ...,
    ): ...
    def update_tombstone(
        self, identity: Identity, id_: str, data, expand: bool = ..., uow=None
    ): ...
    def cleanup_record(self, identity: Identity, id_: str, uow=None): ...
    def restore_record(
        self, identity: Identity, id_: str, expand: bool = ..., uow=None
    ): ...
    def mark_record_for_purge(
        self, identity: Identity, id_: str, expand: bool = ..., uow=None
    ): ...
    def unmark_record_for_purge(
        self, identity: Identity, id_: str, expand: bool = ..., uow=None
    ): ...
    def purge_record(self, identity: Identity, id_: str, uow=None): ...
    def publish(self, identity: Identity, id_: str, uow=None, expand: bool = ...): ...

    # Note: keep base search() signature to avoid incompatible override.
    def search_drafts(
        self,
        identity: Identity,
        params: Optional[dict[str, Any]] = ...,
        search_preference: Optional[str] = ...,
        expand: bool = ...,
        extra_filter=None,
        **kwargs,
    ): ...
    def search_versions(
        self,
        identity: Identity,
        id_: str,
        params: Optional[dict[str, Any]] = ...,
        search_preference: Optional[str] = ...,
        expand: bool = ...,
        permission_action: str = ...,
        **kwargs,
    ): ...
    def scan_versions(
        self,
        identity: Identity,
        id_: str,
        params: Optional[dict[str, Any]] = ...,
        search_preference: Optional[str] = ...,
        expand: bool = ...,
        permission_action: str = ...,
        **kwargs,
    ): ...
    def read(  # type: ignore[override]
        self,
        identity: Identity,
        id_: str,
        expand: bool = False,
        include_deleted: bool = False,
    ): ...
    def read_draft(self, identity: Identity, id_: str, expand: bool = ...): ...
    def update_draft(
        self,
        identity: Identity,
        id_: str,
        data,
        revision_id: Optional[int] = ...,
        uow=None,
        expand: bool = ...,
    ): ...
    def set_quota(
        self,
        identity: Identity,
        id_: str,
        data,
        files_attr: str = ...,
        uow=None,
    ) -> bool: ...
    def set_user_quota(self, identity: Identity, id_: str, data, uow=None) -> bool: ...
    def search_revisions(self, identity: Identity, id_): ...
    def read_revision(
        self,
        identity: Identity,
        id_: str,
        revision_id: str,
        include_previous: bool = ...,
    ): ...
