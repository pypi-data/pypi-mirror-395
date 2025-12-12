from typing import Any, Callable, ParamSpec, TypeVar

from invenio_records_resources.services.errors import PermissionDeniedError

P = ParamSpec("P")
R = TypeVar("R")

def groups_enabled(
    group_subject_type: str, **kwargs: Any
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

__all__ = ("groups_enabled", "PermissionDeniedError")
