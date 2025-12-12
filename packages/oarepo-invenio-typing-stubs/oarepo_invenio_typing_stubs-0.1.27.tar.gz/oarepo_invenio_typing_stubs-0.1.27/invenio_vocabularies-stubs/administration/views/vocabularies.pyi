from typing import Any, Dict

from flask_babel import LazyString
from invenio_administration.views.base import AdminResourceListView

class VocabulariesListView(AdminResourceListView):
    api_endpoint: str
    name: str
    menu_label: LazyString
    resource_config: str
    search_request_headers: Dict[str, str]
    title: LazyString
    category: LazyString
    pid_path: str
    icon: str
    template: str
    display_search: bool
    display_delete: bool
    display_edit: bool
    display_create: bool
    item_field_list: Dict[str, Dict[str, Any]]
    search_config_name: str
    search_facets_config_name: str
    search_sort_config_name: str
