from typing import Any, List

from invenio_access import any_user as any_user
from invenio_access import authenticated_user as authenticated_user
from invenio_records_permissions.generators import ConditionalGenerator, Generator
from invenio_search.engine import dsl

class IfTags(ConditionalGenerator):
    tags: List[str]
    def __init__(
        self,
        tags: list[str],
        then_: list[Generator] | tuple[Generator, ...],
        else_: list[Generator] | tuple[Generator, ...],
    ) -> None: ...
    def _condition(
        self, record: dict[str, Any] | None = ..., **kwargs: Any
    ) -> bool: ...
    def query_filter(self, **kwargs: Any) -> dsl.query.Query: ...
