from collections.abc import Mapping
from typing import Any

from invenio_communities.communities.records.api import Community
from invenio_drafts_resources.services.records.config import (
    RecordServiceConfig,
    SearchDraftsOptions,
    SearchOptions,
    SearchVersionsOptions,
)
from invenio_indexer.api import RecordIndexer
from invenio_rdm_records.records.api import RDMRecord
from invenio_rdm_records.services.customizations import (
    FromConfigConditionalPIDs,
    FromConfigPIDsProviders,
    FromConfigRequiredPIDs,
)
from invenio_rdm_records.services.permissions import (
    RDMRecordPermissionPolicy,
)
from invenio_rdm_records.services.result_items import (
    GrantItem,
    GrantList,
    SecretLinkItem,
    SecretLinkList,
)
from invenio_rdm_records.services.results import RDMRecordRevisionsList
from invenio_rdm_records.services.schemas.community_records import (
    CommunityRecordsSchema,
)
from invenio_rdm_records.services.schemas.parent.access import (
    AccessSettingsSchema,
    RequestAccessSchema,
)
from invenio_rdm_records.services.schemas.parent.access import (
    Grant as GrantSchema,
)
from invenio_rdm_records.services.schemas.parent.access import (
    Grants as GrantsSchema,
)
from invenio_rdm_records.services.schemas.parent.access import (
    SecretLink as SecretLinkSchema,
)
from invenio_rdm_records.services.schemas.quota import QuotaSchema
from invenio_rdm_records.services.schemas.tombstone import TombstoneSchema
from invenio_records_resources.services import (
    FileServiceConfig as BaseFileServiceConfig,
)
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    SearchOptionsMixin,
    ServiceConfig,
)
from invenio_records_resources.services.base.links import (
    ConditionalLink,
    EndpointLink,
    ExternalLink,
    NestedLinks,
)
from invenio_records_resources.services.records.config import (
    RecordServiceConfig as BaseRecordServiceConfig,
)

def is_draft_and_has_review(record, ctx): ...
def is_record_and_has_doi(record, ctx): ...
def is_record_or_draft_and_has_parent_doi(record, ctx): ...
def has_doi(record, ctx): ...
def is_iiif_compatible(file_, ctx): ...
def archive_download_enabled(record, ctx): ...
def _groups_enabled(record, ctx): ...
def is_datacite_test(record, ctx): ...
def lock_edit_published_files(service, identity, record=None, draft=None): ...
def has_image_files(record, ctx): ...
def record_thumbnail_sizes() -> list[int]: ...
def get_record_thumbnail_file(record, **kwargs) -> str | None: ...

class RDMSearchOptions(SearchOptions, SearchOptionsMixin):
    # NOTE: immutable defaults prevent shared-state mutation across configs.
    verified_sorting_enabled: bool

class RDMCommunityRecordSearchOptions(RDMSearchOptions):
    verified_sorting_enabled: bool

class RDMSearchDraftsOptions(SearchDraftsOptions, SearchOptionsMixin):
    facets: Mapping[str, Any]
    params_interpreters_cls: tuple[type, ...]

class RDMSearchVersionsOptions(SearchVersionsOptions, SearchOptionsMixin):
    params_interpreters_cls: tuple[type, ...]

class RecordPIDLink(ExternalLink):
    def vars(self, record, vars: dict[str, Any]) -> None: ...

class ThumbnailLinks:
    link_for_thumbnail: EndpointLink
    def __init__(
        self, sizes: list[int] | None = None, when: Any | None = None
    ) -> None: ...
    def should_render(self, obj: Any, context: dict[str, Any]) -> bool: ...
    def expand(self, obj: Any, context: dict[str, Any]) -> dict[str, str]: ...

record_doi_link: ConditionalLink

def vars_preview_html(drafcord, vars: dict[str, Any]) -> None: ...
def get_pid_value(drafcord) -> str | None: ...
def is_record_or_draft(drafcord) -> str: ...
def get_iiif_uuid_of_drafcord_from_file_drafcord(
    file_drafcord, vars: dict[str, Any]
) -> str: ...
def get_iiif_uuid_of_file_drafcord(file_drafcord, vars: dict[str, Any]) -> str: ...
def get_iiif_uuid_of_drafcord(drafcord, vars: dict[str, Any]) -> str: ...
def vars_self_iiif(drafcord, vars: dict[str, Any]) -> None: ...

class WithFileLinks(type): ...

class FileServiceConfig(
    BaseFileServiceConfig, ConfiguratorMixin, metaclass=WithFileLinks
):
    # NOTE: configs expose immutable defaults so subclasses override safely.
    name_of_file_blueprint: str

class RDMFileRecordServiceConfig(FileServiceConfig, ConfiguratorMixin): ...

class RDMRecordServiceConfig(RecordServiceConfig, ConfiguratorMixin):
    # NOTE: immutable defaults to avoid shared mutable state between configs.
    schema_access_settings: type[AccessSettingsSchema]
    schema_secret_link: type[SecretLinkSchema]
    schema_grant: type[GrantSchema]
    schema_grants: type[GrantsSchema]
    schema_request_access: type[RequestAccessSchema]
    schema_tombstone: type[TombstoneSchema]
    schema_quota: type[QuotaSchema]
    link_result_item_cls: type[SecretLinkItem]
    link_result_list_cls: type[SecretLinkList]
    grant_result_item_cls: type[GrantItem]
    grant_result_list_cls: type[GrantList]
    revision_result_list_cls: type[RDMRecordRevisionsList]
    pids_providers: FromConfigPIDsProviders
    pids_required: FromConfigRequiredPIDs
    parent_pids_providers: FromConfigPIDsProviders
    parent_pids_required: FromConfigRequiredPIDs
    parent_pids_conditional: FromConfigConditionalPIDs
    nested_links_item: tuple[NestedLinks, ...]
    record_file_processors: tuple[Any, ...]

class RDMCommunityRecordsConfig(
    BaseRecordServiceConfig[
        RDMRecord,
        RDMCommunityRecordSearchOptions,
        CommunityRecordsSchema,
        RecordIndexer,
        RDMRecordPermissionPolicy,
    ],
    ConfiguratorMixin,
):
    # NOTE: immutable defaults to ensure overrides happen via replacement.
    community_cls: type[Community]
    search_versions: type[RDMSearchVersionsOptions]
    community_record_schema: type[CommunityRecordsSchema]
    max_number_of_removals: int
    links_search_community_records: Mapping[str, Any]

class RDMRecordMediaFilesServiceConfig(RDMRecordServiceConfig): ...
class RDMMediaFileRecordServiceConfig(FileServiceConfig, ConfiguratorMixin): ...
class RDMFileDraftServiceConfig(FileServiceConfig, ConfiguratorMixin): ...
class RDMRecordCommunitiesConfig(ServiceConfig, ConfiguratorMixin): ...
class RDMRecordRequestsConfig(ServiceConfig, ConfiguratorMixin): ...
