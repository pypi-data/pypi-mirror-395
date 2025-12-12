from datetime import timedelta
from typing import Any, Callable

from invenio_communities.cache.cache import IdentityCache
from invenio_communities.communities.records.systemfields.access import (
    RecordSubmissionPolicyEnum as RecordSubmissionPolicyEnum,
)
from invenio_communities.communities.services import facets as facets

COMMUNITIES_ROUTES: dict[str, str]
COMMUNITIES_FACETS: dict[str, dict[str, Any]]
COMMUNITIES_SUBCOMMUNITIES_FACETS = COMMUNITIES_FACETS
COMMUNITIES_SORT_OPTIONS: dict[str, dict[str, Any]]
COMMUNITIES_ROLES: list[dict[str, Any]]
COMMUNITIES_SEARCH: dict[str, list[str]]
COMMUNITIES_SEARCH_SORT_BY_VERIFIED: bool
COMMUNITIES_SUBCOMMUNITIES_SEARCH: dict[str, list[str]]
COMMUNITIES_REQUESTS_SEARCH: dict[str, list[str]]
COMMUNITIES_MEMBERS_SEARCH: dict[str, list[str]]
COMMUNITIES_MEMBERS_SORT_OPTIONS: dict[str, dict[str, Any]]
COMMUNITIES_MEMBERS_FACETS: dict[str, dict[str, Any]]
COMMUNITIES_INVITATIONS_SEARCH: dict[str, list[str]]
COMMUNITIES_INVITATIONS_SORT_OPTIONS: dict[str, dict[str, Any]]
COMMUNITIES_INVITATIONS_EXPIRES_IN: timedelta
COMMUNITIES_LOGO_MAX_FILE_SIZE: int
COMMUNITIES_NAMESPACES: dict[str, str]
COMMUNITIES_CUSTOM_FIELDS: list[Any]
COMMUNITIES_CUSTOM_FIELDS_UI: list[Any]
COMMUNITIES_ALLOW_RESTRICTED: bool
COMMUNITIES_IDENTITIES_CACHE_TIME: int
COMMUNITIES_IDENTITIES_CACHE_REDIS_URL: str
COMMUNITIES_IDENTITIES_CACHE_HANDLER: str | Callable[[Any], IdentityCache]
COMMUNITIES_OAI_SETS_PREFIX: str
COMMUNITIES_ALWAYS_SHOW_CREATE_LINK: bool
COMMUNITIES_ALLOW_MEMBERSHIP_REQUESTS: bool
COMMUNITIES_DEFAULT_RECORD_SUBMISSION_POLICY: RecordSubmissionPolicyEnum
