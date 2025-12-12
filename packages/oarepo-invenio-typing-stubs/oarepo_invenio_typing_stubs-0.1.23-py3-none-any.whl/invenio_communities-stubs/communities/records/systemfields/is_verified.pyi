from typing import Any, Optional, Self, overload

from invenio_communities.communities.records.api import Community
from invenio_records_resources.records.systemfields.calculated import (
    CalculatedIndexedField,
)

class IsVerifiedField(CalculatedIndexedField):
    def __init__(self, key: Optional[str] = None, **kwargs: Any) -> None: ...
    def calculate(self, record: Community) -> bool: ...  # type: ignore[override]
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Community]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Community, owner: type[Community]
    ) -> bool: ...
    def __set__(self, instance: Community, value: bool) -> None: ...  # type: ignore[override]
