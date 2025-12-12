from __future__ import annotations

from typing import Any, Callable, Tuple

from flask_admin.contrib.sqla import ModelView  # type: ignore[reportMissingTypeStubs,import-not-found]
from invenio_admin.filters import FilterConverter  # type: ignore[reportMissingTypeStubs,import-not-found]
from invenio_records.models import RecordMetadata

class RecordMetadataModelView(ModelView):
    filter_converter: FilterConverter
    can_create: bool
    can_edit: bool
    can_delete: bool
    can_view_details: bool
    column_list: Tuple[str, ...]
    column_details_list: Tuple[str, ...]
    column_labels: dict[str, Any]
    column_formatters: dict[str, Callable[..., Any]]
    column_filters: Tuple[str, ...]
    column_default_sort: Tuple[str, bool]
    page_size: int

    def delete_model(self, model: RecordMetadata) -> bool: ...

record_adminview: dict[str, Any]
