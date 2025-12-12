from typing import Any, Dict

from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceListView,
)
from invenio_communities.communities.schema import (
    CommunityFeaturedSchema as CommunityFeaturedSchema,
)

class CommunityListView(AdminResourceListView):
    api_endpoint: str
    name: str
    resource_config: str
    search_request_headers: Dict[str, str]  # HTTP headers dict
    title: str
    menu_label: str
    category: str
    pid_path: str
    icon: str
    template: str
    display_search: bool
    display_delete: bool
    display_create: bool
    display_edit: bool
    item_field_list: Dict[str, Dict[str, Any]]  # Field configuration dict
    actions: Dict[str, Dict[str, Any]]  # Actions configuration dict
    search_config_name: str
    search_facets_config_name: str
    search_sort_config_name: str
    def init_search_config(self): ...

class CommunityDetailView(AdminResourceDetailView):
    url: str
    api_endpoint: str
    name: str
    resource_config: str
    title: str
    template: str
    display_delete: bool
    display_edit: bool
    list_view_name: str
    pid_path: str
    request_headers: Dict[str, str]  # HTTP headers dict
    actions: Dict[str, Dict[str, Any]]  # Actions configuration dict
    item_field_list: Dict[str, Dict[str, Any]]  # Field configuration dict
