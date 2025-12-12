from typing import Any

from flask_principal import PermissionDenied

class RDMRecordsException(Exception): ...

class GrantExistsError(RDMRecordsException):
    description: str

class RecordDeletedException(RDMRecordsException):
    record: Any
    result_item: Any | None
    def __init__(self, record, result_item: Any | None = None) -> None: ...

class DeletionStatusException(RDMRecordsException):
    expected_status: Any
    record: Any
    def __init__(self, record, expected_status) -> None: ...

class EmbargoNotLiftedError(RDMRecordsException):
    record_id: Any
    def __init__(self, record_id) -> None: ...
    @property
    def description(self) -> str: ...

class ReviewException(RDMRecordsException): ...

class ReviewNotFoundError(ReviewException):
    description: str

class ReviewStateError(ReviewException): ...
class ReviewExistsError(ReviewException): ...
class CommunitySubmissionException(Exception): ...

class CommunityAlreadyExists(CommunitySubmissionException):
    description: str

class CommunityInclusionException(Exception): ...

class InvalidAccessRestrictions(CommunityInclusionException):
    description: str

class OpenRequestAlreadyExists(CommunitySubmissionException):
    request_id: Any
    def __init__(self, request_id) -> None: ...
    @property
    def description(self) -> str: ...

class ValidationErrorWithMessageAsList(Exception):
    messages: list[dict[str, list[str]]]
    def __init__(self, message: list[dict[str, list[str]]]) -> None: ...

class RecordCommunityMissing(Exception):
    record_id: Any
    community_id: Any
    def __init__(self, record_id, community_id) -> None: ...
    @property
    def description(self) -> str: ...

class InvalidCommunityVisibility(Exception):
    reason: Any
    def __init__(self, reason) -> None: ...
    @property
    def description(self) -> str: ...

class AccessRequestException(RDMRecordsException): ...

class AccessRequestExistsError(AccessRequestException):
    request_id: Any
    def __init__(self, request_id) -> None: ...
    @property
    def description(self) -> str: ...

class RecordSubmissionClosedCommunityError(PermissionDenied):
    description: str

class CommunityRequiredError(Exception):
    description: str

class CannotRemoveCommunityError(Exception):
    description: str
