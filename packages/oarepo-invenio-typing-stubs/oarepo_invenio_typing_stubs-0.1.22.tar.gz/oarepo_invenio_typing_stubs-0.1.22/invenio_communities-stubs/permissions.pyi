from typing import Optional, TypedDict

from flask_principal import Identity
from invenio_communities.communities.records.api import Community
from invenio_communities.generators import AllowedMemberTypes as AllowedMemberTypes
from invenio_communities.generators import (
    AuthenticatedButNotCommunityMembers as AuthenticatedButNotCommunityMembers,
)
from invenio_communities.generators import CommunityCurators as CommunityCurators
from invenio_communities.generators import CommunityManagers as CommunityManagers
from invenio_communities.generators import (
    CommunityManagersForRole as CommunityManagersForRole,
)
from invenio_communities.generators import CommunityMembers as CommunityMembers
from invenio_communities.generators import CommunityOwners as CommunityOwners
from invenio_communities.generators import CommunitySelfMember as CommunitySelfMember
from invenio_communities.generators import IfCommunityDeleted as IfCommunityDeleted
from invenio_communities.generators import IfMemberPolicyClosed as IfMemberPolicyClosed
from invenio_communities.generators import (
    IfRecordSubmissionPolicyClosed as IfRecordSubmissionPolicyClosed,
)
from invenio_communities.generators import IfRestricted as IfRestricted
from invenio_communities.generators import ReviewPolicy as ReviewPolicy
from invenio_records_permissions.generators import Generator
from invenio_records_permissions.policies import BasePermissionPolicy

class CommunityPermissionPolicy(BasePermissionPolicy):
    """Permissions for Community CRUD operations."""

    # NOTE: tuples keep the default generator sequences immutable here while
    # still letting subclasses provide their own overrides.
    can_create: tuple[Generator, ...]
    can_read: tuple[Generator, ...]
    can_read_deleted: tuple[Generator, ...]
    can_update: tuple[Generator, ...]
    can_delete: tuple[Generator, ...]
    can_purge: tuple[Generator, ...]
    can_manage_access: tuple[Generator, ...]
    can_create_restricted: tuple[Generator, ...]
    can_search: tuple[Generator, ...]
    can_search_user_communities: tuple[Generator, ...]
    can_search_invites: tuple[Generator, ...]
    can_search_requests: tuple[Generator, ...]
    can_rename: tuple[Generator, ...]
    can_submit_record: tuple[Generator, ...]
    can_include_directly: tuple[Generator, ...]
    can_members_add: tuple[Generator, ...]
    can_members_invite: tuple[Generator, ...]
    can_members_manage: tuple[Generator, ...]
    can_members_search: tuple[Generator, ...]
    can_members_search_public: tuple[Generator, ...]
    can_members_bulk_update: tuple[Generator, ...]
    can_members_bulk_delete = can_members_bulk_update
    can_members_update: tuple[Generator, ...]
    can_members_delete = can_members_update
    can_invite_owners: tuple[Generator, ...]
    can_featured_search: tuple[Generator, ...]
    can_featured_list: tuple[Generator, ...]
    can_featured_create: tuple[Generator, ...]
    can_featured_update: tuple[Generator, ...]
    can_featured_delete: tuple[Generator, ...]
    can_moderate: tuple[Generator, ...]
    can_set_theme: tuple[Generator, ...]
    can_delete_theme = can_set_theme
    can_manage_children: tuple[Generator, ...]
    can_manage_parent: tuple[Generator, ...]
    can_request_membership: tuple[Generator, ...]

class PermissionContext(TypedDict, total=False):
    action: str
    identity: Optional[Identity]
    permission_policy_cls: type[BasePermissionPolicy]

def can_perform_action(community: Community, context: PermissionContext) -> bool: ...
