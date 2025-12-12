from collections.abc import Mapping
from typing import Any

import marshmallow as ma
from flask_resources import ResourceConfig, ResponseHandler
from invenio_communities.communities.resources import CommunityResourceConfig
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.files import FileResourceConfig
from invenio_records_resources.services.base.config import ConfiguratorMixin
from invenio_requests.resources.requests.config import RequestSearchRequestArgsSchema

def csl_url_args_retriever() -> tuple[str | None, str | None]: ...

record_serializers: Mapping[str, ResponseHandler]
error_handlers: Mapping[type, Any]

class RDMRecordResourceConfig(RecordResourceConfig, ConfiguratorMixin): ...
class RDMRecordFilesResourceConfig(FileResourceConfig, ConfiguratorMixin): ...
class RDMDraftFilesResourceConfig(FileResourceConfig, ConfiguratorMixin): ...
class RDMRecordMediaFilesResourceConfig(FileResourceConfig, ConfiguratorMixin): ...
class RDMDraftMediaFilesResourceConfig(FileResourceConfig, ConfiguratorMixin): ...

record_links_error_handlers: Mapping[type, Any]
grants_error_handlers: Mapping[type, Any]
user_access_error_handlers: Mapping[type, Any]
group_access_error_handlers: Mapping[type, Any]

class RDMParentRecordLinksResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    links_config: Mapping[str, Any]

class RDMParentGrantsResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    links_config: Mapping[str, Any]

class RDMGrantUserAccessResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    links_config: Mapping[str, Any]
    grant_subject_type: str

class RDMGrantGroupAccessResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    links_config: Mapping[str, Any]
    grant_subject_type: str

class RDMCommunityRecordsResourceConfig(RecordResourceConfig, ConfiguratorMixin): ...
class RDMRecordCommunitiesResourceConfig(
    CommunityResourceConfig, ConfiguratorMixin
): ...

class RDMRecordRequestsResourceConfig(ResourceConfig, ConfiguratorMixin):
    # NOTE: configs expose immutable defaults to prevent shared-state mutation.
    request_search_args: type[RequestSearchRequestArgsSchema]
    request_view_args: Mapping[str, ma.fields.Field]
    request_extra_args: Mapping[str, ma.fields.Field]
    response_handlers: Mapping[str, ResponseHandler]
