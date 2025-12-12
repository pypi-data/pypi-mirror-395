from typing import Any, ClassVar, Dict, List, Optional, Tuple

from flask_principal import Identity
from invenio_communities.members.errors import (
    InvalidMemberError as InvalidMemberError,
)
from invenio_communities.members.records.models import (
    ArchivedInvitationModel as ArchivedInvitationModel,
)
from invenio_communities.members.records.models import (
    MemberModel as MemberModel,
)
from invenio_records.dumpers import SearchDumper
from invenio_records.systemfields import DictField
from invenio_records_resources.records import Record
from invenio_records_resources.records.systemfields import IndexField

relations_dumper: SearchDumper

class MemberMixin:
    community_id: Any
    user_id: Any
    group_id: Any
    request_id: Any
    role: Any
    visible: Any
    active: Any
    relations: Any
    @classmethod
    def get_memberships_from_group_ids(
        cls, identity: Identity, group_ids: List[Any]
    ) -> List[Tuple[str, str]]: ...
    @classmethod
    def get_memberships(cls, identity: Identity) -> List[Tuple[str, str]]: ...
    @classmethod
    def get_member_by_request(cls, request_id: str) -> "Member": ...
    @classmethod
    def get_members(
        cls, community_id: str, members: Optional[List[Dict[str, Any]]] = None
    ) -> List["Member"]: ...
    @classmethod
    def has_members(cls, community_id: str, role: Optional[str] = None) -> int: ...

class Member(Record, MemberMixin):
    metadata: ClassVar[DictField]
    index: ClassVar[IndexField]

class ArchivedInvitation(Record, MemberMixin):
    metadata: ClassVar[DictField]
    index: ClassVar[IndexField]
    @classmethod
    def create_from_member(cls, member: "Member") -> "ArchivedInvitation": ...
