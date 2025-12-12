from typing import ClassVar

from invenio_communities.communities.records import models as models
from invenio_communities.communities.records.systemfields.access import (
    CommunityAccessField as CommunityAccessField,
)
from invenio_communities.communities.records.systemfields.children import (
    ChildrenField as ChildrenField,
)
from invenio_communities.communities.records.systemfields.deletion_status import (
    CommunityDeletionStatusField as CommunityDeletionStatusField,
)
from invenio_communities.communities.records.systemfields.is_verified import (
    IsVerifiedField as IsVerifiedField,
)
from invenio_communities.communities.records.systemfields.parent_community import (
    ParentCommunityField as ParentCommunityField,
)
from invenio_communities.communities.records.systemfields.pidslug import (
    PIDSlugField as PIDSlugField,
)
from invenio_communities.communities.records.systemfields.tombstone import (
    TombstoneField as TombstoneField,
)
from invenio_records.dumpers import Dumper
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import ConstantField, DictField, ModelField
from invenio_records.systemfields.relations import MultiRelationsField
from invenio_records_resources.records.api import FileRecord, Record
from invenio_records_resources.records.systemfields import PIDField
from invenio_records_resources.records.systemfields.files.field import FilesField
from invenio_records_resources.records.systemfields.index import IndexField

class CommunityFile(FileRecord):
    model_cls: ClassVar[type[RecordMetadata]]
    record_cls: ClassVar[type[Record]]

class Community(Record):
    pid: ClassVar[PIDField]
    parent: ParentCommunityField
    children: ChildrenField
    slug: ModelField
    schema: ClassVar[ConstantField]
    model_cls: ClassVar[type[RecordMetadata]]
    dumper: ClassVar[Dumper]
    index: ClassVar[IndexField]
    access: ClassVar[CommunityAccessField]
    custom_fields: ClassVar[DictField]
    theme: ClassVar[DictField]
    bucket_id: ClassVar[ModelField]
    bucket: ClassVar[ModelField]
    files: ClassVar[FilesField]
    relations: ClassVar[MultiRelationsField]
    is_verified: ClassVar[IsVerifiedField]
    deletion_status: ClassVar[CommunityDeletionStatusField]
    tombstone: ClassVar[TombstoneField]
