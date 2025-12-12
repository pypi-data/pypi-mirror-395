from typing import Any, ClassVar, Optional

from invenio_communities.communities.records.systemfields.deletion_status import (
    CommunityDeletionStatusEnum as CommunityDeletionStatusEnum,
)
from invenio_records.models import RecordMetadataBase, Timestamp
from invenio_records_resources.records import FileRecordModelMixin

# Note: db.Model base comes from invenio_db.shared.SQLAlchemy.Model; use a placeholder.
class _Model: ...

class CommunityMetadata(_Model, RecordMetadataBase):
    __tablename__: ClassVar[str]
    slug: str
    bucket_id: Any
    bucket: Any
    deletion_status: CommunityDeletionStatusEnum

class CommunityFileMetadata(_Model, RecordMetadataBase, FileRecordModelMixin):
    __record_model_cls__ = CommunityMetadata
    __tablename__: ClassVar[str]

class CommunityFeatured(_Model, Timestamp):
    __tablename__: ClassVar[str]
    id: Any
    community_id: Any
    start_date: Optional[Any]
