from typing import Any, Callable, ClassVar

from flask import Response
from flask_resources import HTTPJSONException
from invenio_records_resources.services.errors import ValidationErrorGroup
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

def create_pid_redirected_error_handler() -> Callable[[Exception], Response]: ...

class HTTPJSONValidationException(HTTPJSONException):
    def __init__(self, exception: ValidationError | ValidationErrorGroup) -> None: ...

class HTTPJSONSearchRequestError(HTTPJSONException):
    causes_responses: ClassVar[dict[str, tuple[int, Any]]]

    def __init__(self, error: Exception) -> None: ...

class ErrorHandlersMixin:
    error_handlers: ClassVar[
        dict[
            int | type[HTTPException] | type[BaseException],
            Callable[[Exception], Response],
        ]
    ]
