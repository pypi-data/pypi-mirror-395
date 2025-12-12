from collections.abc import Mapping
from typing import Any, Callable

from invenio_drafts_resources.records.api import Draft, Record
from invenio_drafts_resources.services.records.components import (
    DraftMetadataComponent as DraftMetadataComponent,
)
from invenio_drafts_resources.services.records.components import (
    PIDComponent as PIDComponent,
)
from invenio_drafts_resources.services.records.permissions import (
    RecordPermissionPolicy as RecordPermissionPolicy,
)
from invenio_drafts_resources.services.records.schema import (
    ParentSchema as ParentSchema,
)
from invenio_drafts_resources.services.records.schema import (
    RecordSchema as RecordSchema,
)
from invenio_drafts_resources.services.records.search_params import (
    AllVersionsParam as AllVersionsParam,
)
from invenio_indexer.api import RecordIndexer  # type: ignore[import-untyped]
from invenio_records_resources.services import EndpointLink, Link
from invenio_records_resources.services import (
    RecordServiceConfig as RecordServiceConfigBase,
)
from invenio_records_resources.services import SearchOptions as SearchOptionsBase

def is_draft(record, ctx): ...
def is_record(record, ctx): ...
def lock_edit_published_files(service, identity, record=None, draft=None): ...

class SearchOptions(SearchOptionsBase):
    # NOTE: immutable defaults ensure overrides swap values without mutating.
    sort_options: Mapping[str, Mapping[str, Any]]
    params_interpreters_cls: tuple[type, ...]

class SearchDraftsOptions(SearchOptions):
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]
    params_interpreters_cls: tuple[type, ...]

class SearchVersionsOptions(SearchOptions):
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]
    facets_options: Mapping[str, Any]
    params_interpreters_cls: tuple[type, ...]

class RecordServiceConfig(
    RecordServiceConfigBase[
        Record,
        SearchOptionsBase,
        RecordSchema,
        RecordIndexer,
        RecordPermissionPolicy,
    ]
):
    # NOTE: configs expose immutable defaults so subclasses override safely.
    draft_cls: type[Draft] | None
    draft_indexer_cls: type[RecordIndexer]
    draft_indexer_queue_name: str
    schema_parent: type[ParentSchema]
    search: type[SearchOptionsBase]
    search_drafts: type[SearchDraftsOptions]
    search_versions: type[SearchVersionsOptions]
    default_files_enabled: bool
    default_media_files_enabled: bool
    lock_edit_published_files: Callable[..., Any]
    links_search_drafts: Mapping[str, Callable[..., Any] | Link | EndpointLink]
    links_search_versions: Mapping[str, Callable[..., Any] | Link | EndpointLink]
