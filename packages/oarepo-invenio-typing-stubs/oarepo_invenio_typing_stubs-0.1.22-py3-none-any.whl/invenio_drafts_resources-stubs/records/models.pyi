from datetime import datetime
from typing import ClassVar, Optional
from uuid import UUID

from invenio_records.models import RecordMetadataBase
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped

class ParentRecordMixin[ParentModel: type]:
    __parent_record_model__: ClassVar[type]
    @declared_attr
    def parent_id(cls) -> Mapped[UUID]: ...
    @declared_attr
    def parent(cls) -> Mapped[ParentModel]: ...
    index: Mapped[Optional[int]]

class ParentRecordStateMixin[ParentModel: type, RecordModel: type, DraftModel: type]:
    __parent_record_model__: ClassVar[type]
    __record_model__: ClassVar[type]
    __draft_model__: ClassVar[type]
    @declared_attr
    def parent_id(cls) -> Mapped[UUID]: ...
    @declared_attr
    def latest_id(cls) -> Mapped[Optional[UUID]]: ...
    latest_index: Mapped[Optional[int]]
    @declared_attr
    def next_draft_id(cls) -> Mapped[Optional[UUID]]: ...

class DraftMetadataBase(RecordMetadataBase):
    fork_version_id: Mapped[Optional[int]]
    expires_at: Mapped[Optional[datetime]]
