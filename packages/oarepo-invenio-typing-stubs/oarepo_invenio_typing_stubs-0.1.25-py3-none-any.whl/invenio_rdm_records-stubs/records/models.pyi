from __future__ import annotations

from typing import Any, ClassVar
from uuid import UUID

from invenio_drafts_resources.records.models import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_records.models import RecordMetadataBase, Timestamp
from invenio_records_resources.records.models import FileRecordModelMixin
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.schema import Column

class _Model: ...  # keep typing base for SQLAlchemy models

class RDMParentMetadata(_Model, RecordMetadataBase):
    __tablename__: ClassVar[str]

class RDMParentCommunity(_Model):
    __tablename__: ClassVar[str]
    __record_model__: ClassVar[type[RDMParentMetadata]]

class RDMRecordMetadata(_Model, RecordMetadataBase, ParentRecordMixin[type]):
    __tablename__: ClassVar[str]
    __parent_record_model__: ClassVar[type[RDMParentMetadata]]
    __versioned__: ClassVar[dict[str, Any]]

    bucket_id: Column[Any]
    bucket: Any
    media_bucket_id: Column[Any]
    media_bucket: Any
    deletion_status: Column[Any]

class RDMFileRecordMetadata(_Model, RecordMetadataBase, FileRecordModelMixin):
    __record_model_cls__: ClassVar[type[RecordMetadataBase] | None]
    __tablename__: ClassVar[str]
    __versioned__: ClassVar[dict[str, Any]]

class RDMMediaFileRecordMetadata(_Model, RecordMetadataBase, FileRecordModelMixin):
    __record_model_cls__: ClassVar[type[RecordMetadataBase] | None]
    __tablename__: ClassVar[str]
    __versioned__: ClassVar[dict[str, Any]]

class RDMDraftMetadata(_Model, DraftMetadataBase, ParentRecordMixin[type]):
    __tablename__: ClassVar[str]
    __parent_record_model__: ClassVar[type[RDMParentMetadata]]

    bucket_id: Column[Any]
    bucket: Any
    media_bucket_id: Column[Any]
    media_bucket: Any

class RDMFileDraftMetadata(_Model, RecordMetadataBase, FileRecordModelMixin):
    __record_model_cls__: ClassVar[type[RecordMetadataBase] | None]
    __tablename__: ClassVar[str]

class RDMMediaFileDraftMetadata(_Model, RecordMetadataBase, FileRecordModelMixin):
    __record_model_cls__: ClassVar[type[RecordMetadataBase] | None]
    __tablename__: ClassVar[str]

class RDMVersionsState(_Model, ParentRecordStateMixin[type, type, type]):
    __tablename__: ClassVar[str]
    __parent_record_model__: ClassVar[type[RDMParentMetadata]]
    __record_model__: ClassVar[type[RDMRecordMetadata]]
    __draft_model__: ClassVar[type[RDMDraftMetadata]]

def default_max_file_size(context: Any) -> Any: ...

class RDMRecordQuota(_Model, Timestamp):
    __tablename__: ClassVar[str]

    id: Mapped[UUID]
    @classmethod
    def parent_id(cls) -> Column[Any]: ...
    user_id: Column[int]
    quota_size: Column[Any]
    max_file_size: Column[Any]
    notes: Column[Any]

class RDMUserQuota(_Model, Timestamp):
    __tablename__: ClassVar[str]

    id: Mapped[UUID]
    @classmethod
    def user_id(cls) -> Column[int]: ...
    quota_size: Column[Any]
    max_file_size: Column[Any]
    notes: Column[Any]
