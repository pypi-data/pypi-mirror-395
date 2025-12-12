from typing import Generator, TypedDict

from _typeshed import Incomplete
from marshmallow.exceptions import ValidationError

class ValidationErrorDict(TypedDict):
    field: str
    messages: list[str]

def _iter_errors_dict(
    message_node: dict[str | int, Incomplete] | list[str] | str,
    fieldpath: str = ...,
) -> Generator[ValidationErrorDict, None, None]: ...
def validation_error_to_list_errors(
    exception: ValidationError,
) -> list[ValidationErrorDict]: ...
