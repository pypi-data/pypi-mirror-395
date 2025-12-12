from datetime import timedelta
from typing import ClassVar, Generator, Literal, overload
from uuid import UUID

from invenio_drafts_resources.records.systemfields import (
    ParentField as ParentField,
)
from invenio_drafts_resources.records.systemfields import (
    VersionsField as VersionsField,
)
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import ModelField
from invenio_records_resources.records import Record as RecordBase
from invenio_records_resources.records.systemfields import (
    PIDField,
    PIDStatusCheckField,
)

class DraftRecordIdProviderV2(RecordIdProviderV2):
    default_status_with_obj: ClassVar[PIDStatus]

class ParentRecord(RecordBase):
    model_cls: ClassVar[type[RecordMetadata]]
    pid: ClassVar[PIDField]

class Record(RecordBase):
    is_draft: ClassVar[bool]
    model_cls: ClassVar[type[RecordMetadata]]
    versions_model_cls: ClassVar[type | None]
    parent_record_cls: ClassVar[type["ParentRecord"] | None]
    pid: ClassVar[PIDField]
    is_published: ClassVar[PIDStatusCheckField]
    parent: ClassVar[ParentField]
    versions: ClassVar[VersionsField]
    @overload
    @classmethod
    def get_records_by_parent(
        cls, parent: "ParentRecord", with_deleted: bool = True
    ) -> Generator["Record", None, None]: ...  # keep typing as there are two branches
    @overload
    @classmethod
    def get_records_by_parent(
        cls,
        parent: "ParentRecord",
        with_deleted: bool,
        ids_only: Literal[True],
    ) -> Generator[UUID, None, None]: ...  # keep typing as there are two branches
    @overload
    @classmethod
    def get_records_by_parent(
        cls,
        parent: "ParentRecord",
        with_deleted: bool,
        ids_only: Literal[False],
    ) -> Generator["Record", None, None]: ...
    @classmethod
    def get_latest_by_parent(
        cls, parent: "ParentRecord", id_only: bool = ...
    ) -> "Record" | UUID | None: ...
    @classmethod
    def publish(cls, draft: "Draft") -> "Record": ...
    def register(self) -> None: ...

class Draft(Record):
    is_draft: ClassVar[bool]
    model_cls: ClassVar[type[RecordMetadata]]
    versions_model_cls: ClassVar[type | None]
    parent_record_cls: ClassVar[type["ParentRecord"] | None]
    pid: ClassVar[PIDField]
    parent: ClassVar[ParentField]
    versions: ClassVar[VersionsField]
    expires_at: ClassVar[ModelField]
    fork_version_id: ClassVar[ModelField]

    @classmethod
    def new_version(cls, record: "Record") -> "Draft": ...
    @classmethod
    def edit(cls, record: "Record") -> "Draft": ...
    @classmethod
    def cleanup_drafts(cls, td: timedelta, search_gc_deletes: int = ...) -> None: ...
