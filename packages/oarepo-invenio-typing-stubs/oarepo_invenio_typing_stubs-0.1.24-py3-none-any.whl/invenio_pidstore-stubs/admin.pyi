"""Admin model views for PersistentIdentifier.

Type stubs for invenio_pidstore.admin.
"""

from typing import Any, Dict, Tuple
from uuid import UUID as UUID

from markupsafe import Markup as Markup

def _(x: str) -> str: ...
def object_formatter(v: Any, c: Any, m: Any, p: Any) -> Markup | str: ...

class FilterUUID:
    """UUID aware filter."""

    def apply(self, query: Any, value: str, alias: Any) -> Any: ...

class PersistentIdentifierModelView:
    """ModelView for the PersistentIdentifier."""

    can_create: bool
    can_edit: bool
    can_delete: bool
    can_view_details: bool
    column_display_all_relations: bool
    column_list: Tuple[str, ...]
    column_labels: Dict[str, str]
    column_filters: Tuple[Any, ...]
    column_searchable_list: Tuple[str, ...]
    column_default_sort: Tuple[str, bool]
    column_formatters: Dict[str, Any]
    page_size: int

pid_adminview: Dict[str, Any]
