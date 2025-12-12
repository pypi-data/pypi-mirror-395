from typing import Any, Collection, Iterable, Optional

from flask_principal import Identity, Need
from invenio_records.api import Record
from invenio_records_permissions.generators import ConditionalGenerator, Generator
from invenio_search.engine import dsl

class IfRestricted(ConditionalGenerator):
    field: str
    def __init__(
        self, field: str, then_: Iterable[Generator], else_: Iterable[Generator]
    ) -> None: ...
    def query_filter(
        self, **kwargs: Any
    ) -> dsl.query.Query | list[dsl.query.Query] | None: ...
    def _condition(self, **kwargs: Any) -> bool: ...

class IfDraft(ConditionalGenerator):
    def _condition(self, **kwargs: Any) -> bool: ...

class IfNewRecord(ConditionalGenerator):
    def _condition(self, **kwargs: Any) -> bool: ...

class IfExternalDOIRecord(ConditionalGenerator):
    def _condition(self, **kwargs: Any) -> bool: ...

class IfDeleted(ConditionalGenerator):
    def _condition(self, **kwargs: Any) -> bool: ...

class IfRecordDeleted(Generator):
    then_: Iterable[Generator]
    else_: Iterable[Generator]
    def __init__(
        self, then_: Iterable[Generator], else_: Iterable[Generator]
    ) -> None: ...
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...
    def excludes(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...
    def query_filter(
        self, **kwargs: Any
    ) -> dsl.query.Query | list[dsl.query.Query] | None: ...

class RecordOwners(Generator):
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | list[dsl.query.Query] | None: ...

class AccessGrant(Generator):
    def __init__(self, permission: str) -> None: ...
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | list[dsl.query.Query] | None: ...

class SecretLinks(Generator):
    def __init__(self, permission: str) -> None: ...
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | list[dsl.query.Query] | None: ...

class SubmissionReviewer(Generator):
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...

class RequestReviewers(Generator):
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...

class CommunityInclusionReviewers(Generator):
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...

class RecordCommunitiesAction(Generator):
    def __init__(self, action: str) -> None: ...
    def roles(self, **kwargs: Any) -> set[str]: ...
    def communities(self, identity: Identity) -> list[str]: ...
    def needs(
        self, record: Optional[Record] = ..., **kwargs: Any
    ) -> Collection[Need]: ...
    def query_filter(
        self, identity: Optional[Identity] = ..., **kwargs: Any
    ) -> dsl.query.Query | list[dsl.query.Query] | None: ...

class ResourceAccessToken(Generator):
    def __init__(self, access: str) -> None: ...
    def needs(
        self, record: Optional[Record] = ..., file_key: str | None = ..., **kwargs: Any
    ) -> Collection[Need]: ...

class IfCreate(ConditionalGenerator):
    def _condition(self, **kwargs: Any) -> bool: ...

class IfRequestType(ConditionalGenerator):
    def __init__(
        self, request_type: type, then_: Iterable[Generator], else_: Iterable[Generator]
    ) -> None: ...
    def _condition(self, **kwargs: Any) -> bool: ...

class GuestAccessRequestToken(Generator):
    def needs(self, request: Any | None = ..., **kwargs: Any) -> Collection[Need]: ...

class IfOneCommunity(ConditionalGenerator):
    def _condition(self, **kwargs: Any) -> bool: ...

class IfAtLeastOneCommunity(ConditionalGenerator):
    def _condition(self, **kwargs: Any) -> bool: ...

# Helper names used elsewhere
CommunityInclusionNeed: Any
