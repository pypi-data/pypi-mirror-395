from __future__ import annotations

from typing import Any, Mapping

from _typeshed import Incomplete
from flask_principal import Identity
from invenio_records_resources.services.records.params.base import ParamInterpreter
from invenio_search import RecordsSearchV2

class SortParam(ParamInterpreter):
    def _compute_sort_fields(self, params: Mapping[str, Incomplete]) -> list[str]: ...
    def _default_sort(
        self,
        params: dict[str, Any],
        options: dict[str, Any],
    ) -> str: ...
    def _handle_empty_query(
        self,
        params: dict[str, Any],
        options: dict[str, Any],
    ) -> str: ...
    def apply(
        self,
        identity: Identity,
        search: RecordsSearchV2,
        params: dict[str, Any],
    ) -> RecordsSearchV2: ...
