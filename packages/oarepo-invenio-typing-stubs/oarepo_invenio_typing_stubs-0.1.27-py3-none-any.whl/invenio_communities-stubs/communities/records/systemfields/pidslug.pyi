from typing import Any, Optional, Self, overload
from uuid import UUID

from invenio_communities.communities.records.api import Community
from invenio_records.systemfields import SystemField, SystemFieldContext
from invenio_records_resources.records.api import PersistentIdentifierWrapper

class PIDSlugFieldContext(SystemFieldContext):
    def parse_pid(self, value: Any) -> UUID | str: ...
    def resolve(self, pid_value: Any, registered_only: bool = True) -> Community: ...

class PIDSlugField(SystemField):  # type: ignore[misc]
    def __init__(self, id_field: str, slug_field: str) -> None: ...
    def obj(self, record: Community) -> Optional[PersistentIdentifierWrapper]: ...
    def pre_commit(self, record: Community) -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Community]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Community, owner: type[Community]
    ) -> Optional[PersistentIdentifierWrapper]: ...
    def __set__(self, instance: Community, value: Optional[PersistentIdentifierWrapper]) -> None: ...  # type: ignore[override]
