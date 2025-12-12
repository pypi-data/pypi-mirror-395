from typing import Any, ClassVar

from invenio_administration.views.base import (
    AdminResourceCreateView,
    AdminResourceDetailView,
    AdminResourceEditView,
    AdminResourceListView,
)

class OaiPmhListView(AdminResourceListView):
    api_endpoint: ClassVar[str]
    name: ClassVar[str]
    resource_config: ClassVar[str]
    search_request_headers: ClassVar[dict[str, str]]
    title: ClassVar[Any]
    category: ClassVar[Any]
    pid_path: ClassVar[str]
    icon: ClassVar[str]
    template: ClassVar[str]
    display_search: ClassVar[bool]
    display_delete: ClassVar[bool]
    display_edit: ClassVar[bool]
    item_field_list: ClassVar[dict[str, dict[str, Any]]]
    search_config_name: ClassVar[str]
    search_facets_config_name: ClassVar[str]
    search_sort_config_name: ClassVar[str]
    create_view_name: ClassVar[str]
    resource_name: ClassVar[str]

class OaiPmhEditView(AdminResourceEditView):
    name: ClassVar[str]
    url: ClassVar[str]
    resource_config: ClassVar[str]
    pid_path: ClassVar[str]
    api_endpoint: ClassVar[str]
    title: ClassVar[Any]
    list_view_name: ClassVar[Any]
    form_fields: ClassVar[dict[str, dict[str, Any]]]

class OaiPmhCreateView(AdminResourceCreateView):
    name: ClassVar[str]
    url: ClassVar[str]
    resource_config: ClassVar[str]
    pid_path: ClassVar[str]
    api_endpoint: ClassVar[str]
    title: ClassVar[Any]
    list_view_name: ClassVar[Any]
    form_fields: ClassVar[dict[str, dict[str, Any]]]

class OaiPmhDetailView(AdminResourceDetailView):
    url: ClassVar[str]
    api_endpoint: ClassVar[str]
    search_request_headers: ClassVar[dict[str, str]]
    name: ClassVar[str]
    resource_config: ClassVar[str]
    title: ClassVar[Any]
    template: ClassVar[str]
    display_delete: ClassVar[bool]
    display_edit: ClassVar[bool]
    list_view_name: ClassVar[Any]
    pid_path: ClassVar[str]
    item_field_list: ClassVar[dict[str, dict[str, Any]]]
