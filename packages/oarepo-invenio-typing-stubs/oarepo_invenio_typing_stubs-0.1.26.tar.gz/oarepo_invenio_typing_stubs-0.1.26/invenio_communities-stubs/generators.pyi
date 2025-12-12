from typing import Any, Callable, List, NamedTuple, Optional, Sequence

from flask_principal import Identity, Need
from invenio_communities.communities.records.systemfields.deletion_status import (
    CommunityDeletionStatusEnum as CommunityDeletionStatusEnum,
)
from invenio_communities.members.records.api import Member
from invenio_communities.proxies import current_roles as current_roles
from invenio_records_permissions.generators import Generator
from invenio_search.engine import dsl

class _Need(NamedTuple):
    method: str
    value: str
    role: str

CommunityRoleNeed: Callable[[str, str], Need]

class IfRestrictedBase(Generator):
    field_getter: Callable[[Any], Any]
    field_name: str
    then_value: str
    else_value: str
    then_: List[Generator]
    else_: List[Generator]
    def __init__(
        self,
        field_getter: Callable[[Any], Any],
        field_name: str,
        then_value: str,
        else_value: str,
        then_: List[Generator],
        else_: List[Generator],
    ) -> None: ...
    def generators(self, record: Any) -> List[Generator]: ...
    def needs(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...
    def excludes(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...
    def make_query(
        self, generators: List[Generator], **kwargs: Any
    ) -> dsl.query.Query | None: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | None: ...

class IfRestricted(IfRestrictedBase):
    def __init__(
        self, field: str, then_: List[Generator], else_: List[Generator]
    ) -> None: ...

class ReviewPolicy(Generator):
    closed_: List[Generator]
    open_: List[Generator]
    members_: List[Generator]
    def __init__(
        self,
        closed_: List[Generator],
        open_: List[Generator],
        members_: List[Generator],
    ) -> None: ...
    def needs(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...
    def excludes(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...

class IfRecordSubmissionPolicyClosed(IfRestrictedBase):
    def __init__(self, then_: List[Generator], else_: List[Generator]) -> None: ...

class IfMemberPolicyClosed(IfRestrictedBase):
    def __init__(self, then_: List[Generator], else_: List[Generator]) -> None: ...

class IfCommunityDeleted(Generator):
    then_: List[Generator]
    else_: List[Generator]
    def __init__(self, then_: List[Generator], else_: List[Generator]) -> None: ...
    def generators(self, record: Any) -> List[Generator]: ...
    def needs(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...
    def excludes(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...
    def make_query(
        self, generators: List[Generator], **kwargs: Any
    ) -> dsl.query.Query | None: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | None: ...

class AuthenticatedButNotCommunityMembers(Generator):
    def needs(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...
    def excludes(self, record: Any = ..., **kwargs: Any) -> Sequence[Need]: ...

class CommunityRoles(Generator):
    def roles(self, **kwargs: Any) -> List[str]: ...
    def communities(self, identity: Identity) -> List[str]: ...
    def needs(
        self, record: Any = ..., community_id: Optional[str] = ..., **kwargs: Any
    ) -> Sequence[Need]: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | None: ...

class CommunityMembers(CommunityRoles):
    def roles(self, **kwargs: Any) -> List[str]: ...
    def communities(self, identity: Identity) -> List[str]: ...

class CommunityCurators(CommunityRoles):
    def roles(self, **kwargs: Any) -> List[str]: ...

class CommunityManagers(CommunityRoles):
    def roles(self, **kwargs: Any) -> List[str]: ...

class CommunityManagersForRole(CommunityRoles):
    def roles(
        self, role: Optional[str] = ..., member: Optional[Member] = ..., **kwargs: Any
    ) -> List[str]: ...

class CommunityOwners(CommunityRoles):
    def roles(self, **kwargs: Any) -> List[str]: ...
    def communities(self, identity: Identity) -> List[str]: ...

class CommunitySelfMember(Generator):
    def needs(
        self, member: Optional[Member] = ..., **kwargs: Any
    ) -> Sequence[Need]: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | None: ...

class AllowedMemberTypes(Generator):
    allowed_member_types: tuple[str, ...]
    def __init__(self, *allowed_member_types: str) -> None: ...
    def needs(self, **kwargs: Any) -> Sequence[Need]: ...
    def excludes(
        self, member_types: Optional[List[str]] = ..., **kwargs: Any
    ) -> Sequence[Need]: ...
