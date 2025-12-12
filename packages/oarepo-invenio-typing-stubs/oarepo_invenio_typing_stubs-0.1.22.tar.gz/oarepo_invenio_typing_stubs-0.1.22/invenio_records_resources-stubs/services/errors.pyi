from typing import Any, ClassVar, List, Optional, TypedDict

from flask_principal import PermissionDenied
from invenio_records_resources.records.api import Record
from marshmallow import ValidationError

class RecordPermissionDeniedError(PermissionDenied):
    """Record permission denied error."""

    description: ClassVar[str]
    record: Optional[Record]
    action_name: Optional[str]

    def __init__(
        self,
        action_name: Optional[str] = ...,
        record: Optional[Record] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...

class PermissionDeniedError(PermissionDenied):
    """Permission denied error."""

    @property
    def description(self) -> str: ...

class RevisionIdMismatchError(Exception):
    """Etag check exception."""

    record_revision_id: int
    expected_revision_id: int

    def __init__(self, record_revision_id: int, expected_revision_id: int) -> None: ...
    @property
    def description(self) -> str: ...

class QuerystringValidationError(ValidationError):
    """Error thrown when there is an issue with the querystring."""

    ...

class ValidationErrorGroup(Exception):
    """Error containing multiple validation errors."""

    class FieldValidationError(TypedDict):
        field: str
        messages: List[str]

    errors: List[FieldValidationError]

    def __init__(self, errors: List[FieldValidationError]) -> None: ...

class TransferException(Exception):
    """File transfer exception."""

    ...

class FacetNotFoundError(Exception):
    """Facet not found exception."""

    vocabulary_id: str

    def __init__(self, vocabulary_id: str) -> None: ...

class FileKeyNotFoundError(Exception):
    """Error denoting that a record doesn't have a certain file."""

    recid: str
    file_key: str

    def __init__(self, recid: str, file_key: str) -> None: ...

class FailedFileUploadException(Exception):
    """File failed to upload exception."""

    recid: str
    file_key: str
    file: Any

    def __init__(self, recid: str, file: Any, file_key: str) -> None: ...

class FilesCountExceededException(Exception):
    """Files count is exceeding the max allowed exception."""

    max_files: int
    resulting_files_count: int

    def __init__(self, max_files: int, resulting_files_count: int) -> None: ...
