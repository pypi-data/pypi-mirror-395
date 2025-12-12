from __future__ import annotations

from typing import Any, ClassVar, Optional

from invenio_communities.records.records.systemfields import CommunitiesField
from invenio_drafts_resources.records import Draft
from invenio_drafts_resources.records import Record as DRRecord
from invenio_drafts_resources.records.api import ParentRecord as ParentRecordBase
from invenio_rdm_records.records.systemfields import (
    HasDraftCheckField,
    IsVerifiedField,
    ParentRecordAccessField,
    RecordAccessField,
    RecordDeletionStatusField,
    RecordStatisticsField,
    TombstoneField,
)
from invenio_rdm_records.records.systemfields.draft_status import DraftStatus
from invenio_records.dumpers import Dumper
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import ConstantField, DictField, ModelField
from invenio_records.systemfields.relations import MultiRelationsField
from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.api import Record as RRRecord
from invenio_records_resources.records.systemfields import (
    FilesField,
    IndexField,
    PIDStatusCheckField,
)
from invenio_requests.records.systemfields.relatedrecord import RelatedRecord

class RDMParent(ParentRecordBase):
    model_cls: ClassVar[type[RecordMetadata]]
    dumper: ClassVar[Dumper]

    schema: ClassVar[ConstantField]
    access: ClassVar[ParentRecordAccessField]
    review: ClassVar[RelatedRecord]
    communities: ClassVar[CommunitiesField]
    permission_flags: ClassVar[DictField]
    pids: ClassVar[DictField]
    is_verified: ClassVar[IsVerifiedField]

class RDMFileDraft(FileRecord):
    model_cls: ClassVar[type[RecordMetadata]]
    record_cls: ClassVar[type[RRRecord] | None]

class RDMMediaFileDraft(FileRecord):
    model_cls: ClassVar[type[RecordMetadata]]
    record_cls: ClassVar[type[RRRecord] | None]
    processor: ClassVar[DictField]

def get_files_quota(record: Optional[RDMRecord] = ...) -> dict[str, Any]: ...

get_quota: Any  # alias to get_files_quota

def get_media_files_quota(record: Optional[RDMRecord] = ...) -> dict[str, Any]: ...

class RDMDraft(Draft):
    schema: ClassVar[ConstantField]
    dumper: ClassVar[Dumper]
    relations: ClassVar[MultiRelationsField]

    bucket_id: ClassVar[ModelField]
    bucket: ClassVar[ModelField]
    media_bucket_id: ClassVar[ModelField]
    media_bucket: ClassVar[ModelField]
    access: ClassVar[RecordAccessField]
    is_published: ClassVar[PIDStatusCheckField]
    pids: ClassVar[DictField]
    custom_fields: ClassVar[DictField]

    model_cls: ClassVar[type[RecordMetadata]]
    index: ClassVar[IndexField]
    files: ClassVar[FilesField]
    media_files: ClassVar[FilesField]
    has_draft: ClassVar[HasDraftCheckField]
    status: ClassVar[DraftStatus]

class RDMDraftMediaFiles(RDMDraft):
    files: ClassVar[FilesField]

class RDMFileRecord(FileRecord):
    model_cls: ClassVar[type[RecordMetadata]]
    record_cls: ClassVar[type[RRRecord] | None]

class RDMMediaFileRecord(FileRecord):
    model_cls: ClassVar[type[RecordMetadata]]
    record_cls: ClassVar[type[RRRecord] | None]
    processor: ClassVar[DictField]

class RDMRecord(DRRecord):
    schema: ClassVar[ConstantField]
    dumper: ClassVar[Dumper]
    relations: ClassVar[MultiRelationsField]

    bucket_id: ClassVar[ModelField]
    bucket: ClassVar[ModelField]
    media_bucket_id: ClassVar[ModelField]
    media_bucket: ClassVar[ModelField]
    access: ClassVar[RecordAccessField]
    is_published: ClassVar[PIDStatusCheckField]
    pids: ClassVar[DictField]
    custom_fields: ClassVar[DictField]

    model_cls: ClassVar[type[RecordMetadata]]
    index: ClassVar[IndexField]
    files: ClassVar[FilesField]
    media_files: ClassVar[FilesField]
    has_draft: ClassVar[HasDraftCheckField]
    status: ClassVar[DraftStatus]
    stats: ClassVar[RecordStatisticsField]
    deletion_status: ClassVar[RecordDeletionStatusField]
    tombstone: ClassVar[TombstoneField]

    @classmethod
    def next_latest_published_record_by_parent(
        cls, parent: RDMParent
    ) -> RDMRecord | None: ...
    @classmethod
    def get_latest_published_by_parent(cls, parent: RDMParent) -> RDMRecord | None: ...
    @classmethod
    def get_previous_published_by_parent(
        cls, parent: RDMParent
    ) -> RDMRecord | None: ...

class RDMRecordMediaFiles(RDMRecord):
    files: ClassVar[FilesField]
