from typing import Any, Callable, Generic, ParamSpec, TypeAlias, TypeVar

from invenio_rdm_records.resources.config import (
    RDMCommunityRecordsResourceConfig,
    RDMParentGrantsResourceConfig,
    RDMParentRecordLinksResourceConfig,
    RDMRecordResourceConfig,
)
from invenio_rdm_records.services.access.service import RecordAccessService
from invenio_rdm_records.services.community_records.service import (
    CommunityRecordsService,
)
from invenio_rdm_records.services.services import RDMRecordService
from invenio_records_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.resource import (
    RecordResource,
    request_data,
    request_extra_args,
    request_headers,
    request_read_args,
    request_search_args,
    request_view_args,
)
from invenio_records_resources.services.records.service import RecordService

P = ParamSpec("P")
R = TypeVar("R")
Decorator: TypeAlias = Callable[[Callable[P, R]], Callable[P, R]]
AnyDecorator: TypeAlias = Callable[[Callable[..., Any]], Callable[..., Any]]

# Typed alias for the response_handler decorator factory to avoid Any; keep simple
response_handler: Callable[..., AnyDecorator]

def response_header_signposting(f: Callable[P, R]) -> Callable[P, R]: ...

CRecord = TypeVar("CRecord", bound=RDMRecordResourceConfig)
SRecord = TypeVar("SRecord", bound=RDMRecordService)

class RDMRecordResource(RecordResource[CRecord, SRecord], Generic[CRecord, SRecord]):
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    @request_headers
    @request_extra_args
    @request_view_args
    def search_revisions(self) -> tuple[dict[str, Any], int]: ...
    @request_headers
    @request_extra_args
    @request_read_args
    @request_view_args
    def read_revision(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_read_args
    @request_view_args
    @response_header_signposting
    @response_handler()
    def read(self) -> tuple[dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def set_record_quota(self) -> tuple[dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def set_user_quota(self) -> tuple[dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def delete_record(self) -> tuple[dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def restore_record(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @response_handler()
    def review_read(self) -> tuple[dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def review_update(self) -> tuple[dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    def review_delete(self) -> tuple[str, int]: ...
    @request_headers
    @request_view_args
    @request_data
    def review_submit(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_view_args
    @response_handler()
    def pids_reserve(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_view_args
    @response_handler()
    def pids_discard(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @request_data
    def create_access_request(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @request_data
    def update_access_settings(self) -> tuple[dict[str, Any], int]: ...

class RDMRecordCommunitiesResource(ErrorHandlersMixin):
    def __init__(self, config: Any, service: Any) -> None: ...
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @request_data
    def add(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @request_data
    def remove(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def get_suggestions(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @request_data
    def set_default(self) -> tuple[dict[str, Any], int]: ...

class RDMRecordRequestsResource(ErrorHandlersMixin):
    def __init__(self, config: Any, service: Any) -> None: ...
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self) -> tuple[dict[str, Any], int]: ...

CParentLinks = TypeVar("CParentLinks", bound=RDMParentRecordLinksResourceConfig)
SParentLinks = TypeVar("SParentLinks", bound=RecordService)

class RDMParentRecordLinksResource(
    RecordResource[CParentLinks, SParentLinks], Generic[CParentLinks, SParentLinks]
):
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    @request_view_args
    @request_data
    @response_handler()
    def create(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @response_handler()
    def read(self) -> tuple[dict[str, Any], int]: ...
    def update(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @request_data
    @response_handler()
    def partial_update(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    def delete(self) -> tuple[str, int]: ...
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self) -> tuple[dict[str, Any], int]: ...

CParentGrants = TypeVar("CParentGrants", bound=RDMParentGrantsResourceConfig)
SParentGrants = TypeVar("SParentGrants", bound=RecordAccessService)

class RDMParentGrantsResource(
    RecordResource[CParentGrants, SParentGrants], Generic[CParentGrants, SParentGrants]
):
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    @request_extra_args
    @request_view_args
    @response_handler()
    def read(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_view_args
    @request_data
    @response_handler()
    def create(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_view_args
    @request_data
    @response_handler()
    def update(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_view_args
    @request_data
    @response_handler()
    def partial_update(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    def delete(self) -> tuple[str, int]: ...
    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self) -> tuple[dict[str, Any], int]: ...

CGrantsAccess = TypeVar("CGrantsAccess", bound=RecordResourceConfig)
SGrantsAccess = TypeVar("SGrantsAccess", bound=RecordAccessService)

class RDMGrantsAccessResource(
    RecordResource[CGrantsAccess, SGrantsAccess], Generic[CGrantsAccess, SGrantsAccess]
):
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    @request_extra_args
    @request_view_args
    @response_handler()
    def read(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    def delete(self) -> tuple[str, int]: ...
    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self) -> tuple[dict[str, Any], int]: ...
    @request_extra_args
    @request_view_args
    @request_data
    @response_handler()
    def partial_update(self) -> tuple[dict[str, Any], int]: ...

CCommunityRecords = TypeVar(
    "CCommunityRecords", bound=RDMCommunityRecordsResourceConfig
)
SCommunityRecords = TypeVar("SCommunityRecords", bound=CommunityRecordsService)

class RDMCommunityRecordsResource(
    RecordResource[CCommunityRecords, SCommunityRecords],
    Generic[CCommunityRecords, SCommunityRecords],
):
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self) -> tuple[dict[str, Any], int]: ...
    @request_view_args
    @response_handler()
    @request_data
    def delete(self) -> tuple[dict[str, Any], int]: ...
