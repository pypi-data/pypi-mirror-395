from collections.abc import Mapping
from typing import Any

import marshmallow as ma
from invenio_communities.communities.records.api import Community as Community
from invenio_communities.members.records import Member as Member
from invenio_communities.members.records.api import (
    ArchivedInvitation as ArchivedInvitation,
)
from invenio_communities.members.services import facets as facets
from invenio_communities.members.services.components import (
    CommunityMemberCachingComponent as CommunityMemberCachingComponent,
)
from invenio_indexer.api import RecordIndexer
from invenio_records_permissions.policies import BasePermissionPolicy
from invenio_records_resources.services import RecordServiceConfig, SearchOptions
from invenio_records_resources.services.base.config import ConfiguratorMixin

class PublicSearchOptions(SearchOptions):
    # NOTE: immutable defaults prevent shared-state mutation across configs.
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]
    query_parser_cls: Any

class InvitationsSearchOptions(SearchOptions):
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]
    facets: Mapping[str, Any]

class MemberSearchOptions(PublicSearchOptions):
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]
    facets: Mapping[str, Any]
    query_parser_cls: Any

class MemberServiceConfig(
    RecordServiceConfig[
        Member,
        SearchOptions,
        ma.Schema,
        RecordIndexer,
        BasePermissionPolicy,
    ],
    ConfiguratorMixin,
):
    service_id = "members"
    community_cls = Community
    record_cls = Member
    schema: type[ma.Schema] | None
    indexer_queue_name: str
    relations: Mapping[str, Any]
    archive_cls = ArchivedInvitation
    archive_indexer_cls: Any
    archive_indexer_queue_name: str
    permission_policy_cls: Any
    search: type[SearchOptions]
    search_public: type[SearchOptions]
    search_invitations: type[SearchOptions]
