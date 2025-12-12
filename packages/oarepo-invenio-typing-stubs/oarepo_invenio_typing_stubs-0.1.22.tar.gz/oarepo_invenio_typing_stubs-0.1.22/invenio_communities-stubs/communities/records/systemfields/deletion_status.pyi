import enum
from typing import Any, Optional, Self, overload

from invenio_communities.communities.records.api import Community
from invenio_records.systemfields import SystemField

class CommunityDeletionStatusEnum(enum.Enum):
    PUBLISHED = "P"
    DELETED = "D"
    MARKED = "X"

class CommunityDeletionStatus:
    _status: CommunityDeletionStatusEnum
    def __init__(
        self, status: Optional[CommunityDeletionStatusEnum | str] = None
    ) -> None: ...
    @property
    def status(self) -> str: ...
    @status.setter
    def status(self, value: CommunityDeletionStatusEnum | str | None) -> None: ...
    @property
    def is_deleted(self) -> bool: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: Any) -> bool: ...

class CommunityDeletionStatusField(SystemField):  # type: ignore[misc]
    def pre_commit(self, record: Community) -> None: ...
    def pre_dump(self, *args: Any, **kwargs: Any) -> None: ...
    def post_load(self, *args: Any, **kwargs: Any) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Community]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Community, owner: type[Community]
    ) -> CommunityDeletionStatus: ...
    def __set__(self, instance: Community, value: CommunityDeletionStatus) -> None: ...  # type: ignore[override]
