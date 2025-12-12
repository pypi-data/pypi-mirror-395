from typing import Any

from invenio_communities.generators import CommunityOwners as CommunityOwners
from invenio_communities.subcommunities.services.request import (
    SubCommunityRequest as SubCommunityRequest,
)
from invenio_records_permissions.generators import Generator
from invenio_records_permissions.policies import BasePermissionPolicy
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    FromConfig,
    ServiceConfig,
)
from invenio_records_resources.services.base.results import ServiceItemResult

class SubCommunityPermissionPolicy(BasePermissionPolicy):
    # NOTE: tuples make the defaults immutable while allowing subclasses to
    # redefine them with their own generator tuples.
    can_request_join: tuple[Generator, ...]
    can_read: tuple[Generator, ...]
    can_create: tuple[Generator, ...]
    can_search: tuple[Generator, ...]
    can_update: tuple[Generator, ...]
    can_delete: tuple[Generator, ...]

class SubCommunityServiceConfig(ServiceConfig, ConfiguratorMixin):
    service_id = "subcommunities"
    permission_policy_cls = SubCommunityPermissionPolicy
    result_item_cls: type[ServiceItemResult]
    result_list_cls: Any
    schema: FromConfig
    request_cls: FromConfig
    links_item: dict[str, Any]
