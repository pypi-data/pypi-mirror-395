from typing import Any, ClassVar, List, Optional, Union
from uuid import UUID

from flask_sqlalchemy.query import Query
from invenio_communities.communities.records.models import (
    CommunityMetadata as CommunityMetadata,
)
from invenio_records.models import RecordMetadataBase
from sqlalchemy.ext.declarative import declared_attr

# Note: db.Model base comes from invenio_db; use a local placeholder to avoid dependency typing issues.
class _Model: ...

class BaseMemberModel(RecordMetadataBase):
    id: Any
    @declared_attr
    def community_id(cls): ...
    role: Any
    visible: Any
    @declared_attr
    def user_id(cls): ...
    @declared_attr
    def group_id(cls): ...
    @declared_attr
    def request_id(cls): ...
    active: Any
    @classmethod
    def query_memberships(
        cls,
        user_id: Optional[int] = None,
        group_ids: Optional[List[Union[Any, str]]] = None,
        active: bool = True,
    ) -> Query: ...
    @classmethod
    def count_members(
        cls, community_id: UUID, role: Optional[str] = None, active: bool = True
    ) -> int: ...

class MemberModel(_Model, BaseMemberModel):
    __tablename__: ClassVar[str]
    __table_args__: ClassVar[tuple[Any, ...]]

class ArchivedInvitationModel(_Model, BaseMemberModel):
    __tablename__: ClassVar[str]
    @classmethod
    def from_member_model(
        cls, member_model: MemberModel
    ) -> ArchivedInvitationModel: ...
