from enum import Enum
from typing import Any, Dict, Optional, Self, Type, Union, overload

from invenio_communities.communities.records.api import Community
from invenio_records.systemfields import SystemField

class AccessEnumMixin:
    def __str__(self) -> str: ...
    @classmethod
    def validate(cls, level: Any) -> bool: ...

class VisibilityEnum(AccessEnumMixin, Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"

class MembersVisibilityEnum(AccessEnumMixin, Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"

class MemberPolicyEnum(AccessEnumMixin, Enum):
    OPEN = "open"
    CLOSED = "closed"

class RecordSubmissionPolicyEnum(AccessEnumMixin, Enum):
    OPEN = "open"
    CLOSED = "closed"

class ReviewPolicyEnum(AccessEnumMixin, Enum):
    OPEN = "open"
    CLOSED = "closed"
    MEMBERS = "members"

class CommunityAccess:
    errors: list[str]
    def __init__(
        self,
        visibility: Optional[Union[str, VisibilityEnum]] = None,
        members_visibility: Optional[Union[str, MembersVisibilityEnum]] = None,
        member_policy: Optional[Union[str, MemberPolicyEnum]] = None,
        record_submission_policy: Optional[
            Union[str, RecordSubmissionPolicyEnum]
        ] = None,
        review_policy: Optional[Union[str, ReviewPolicyEnum]] = None,
    ) -> None: ...
    @classmethod
    def validate_visibility_level(cls, level: Union[str, VisibilityEnum]) -> bool: ...
    @classmethod
    def validate_members_visibility_level(
        cls, level: Union[str, MembersVisibilityEnum]
    ) -> bool: ...
    @classmethod
    def validate_member_policy_level(
        cls, level: Union[str, MemberPolicyEnum]
    ) -> bool: ...
    @classmethod
    def validate_record_submission_policy_level(
        cls, level: Union[str, RecordSubmissionPolicyEnum]
    ) -> bool: ...
    @classmethod
    def validate_review_policy_level(
        cls, level: Union[str, ReviewPolicyEnum]
    ) -> bool: ...
    @property
    def visibility(self) -> Union[str, VisibilityEnum]: ...
    @visibility.setter
    def visibility(self, value: Union[str, VisibilityEnum]) -> None: ...
    @property
    def members_visibility(self) -> Union[str, MembersVisibilityEnum]: ...
    @members_visibility.setter
    def members_visibility(self, value: Union[str, MembersVisibilityEnum]) -> None: ...
    @property
    def visibility_is_public(self) -> bool: ...
    @property
    def visibility_is_restricted(self) -> bool: ...
    @property
    def member_policy(self) -> Union[str, MemberPolicyEnum]: ...
    @member_policy.setter
    def member_policy(self, value: Union[str, MemberPolicyEnum]) -> None: ...
    @property
    def record_submission_policy(self) -> Union[str, RecordSubmissionPolicyEnum]: ...
    @record_submission_policy.setter
    def record_submission_policy(
        self, value: Union[str, RecordSubmissionPolicyEnum]
    ) -> None: ...
    @property
    def review_policy(self) -> Union[str, ReviewPolicyEnum]: ...
    @review_policy.setter
    def review_policy(self, value: Union[str, ReviewPolicyEnum]) -> None: ...
    def dump(self) -> Dict[str, str]: ...
    def refresh_from_dict(self, access_dict: Dict[str, str]) -> None: ...
    @classmethod
    def from_dict(cls, access_dict: Dict[str, str]) -> CommunityAccess: ...

class CommunityAccessField(SystemField):
    access_obj_class = CommunityAccess
    def __init__(
        self,
        key: str = "access",
        access_obj_class: Optional[Type[CommunityAccess]] = None,
    ) -> None: ...
    def obj(self, instance: Community) -> CommunityAccess: ...
    def set_obj(self, record: Community, obj: CommunityAccess) -> None: ...
    def pre_commit(self, record: Community) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Self]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Community, owner: type[Community]
    ) -> CommunityAccess: ...
    def __set__(self, instance: Community, value: Any) -> None: ...  # type: ignore[override]

# to override this behaviour.
