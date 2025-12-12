from __future__ import annotations

from typing import Any

from _typeshed import Incomplete
from flask_principal import Identity
from invenio_records_resources.services.records.config import SearchOptions
from invenio_records_resources.services.records.params.base import ParamInterpreter
from invenio_search import RecordsSearchV2

class FacetsParam(ParamInterpreter):
    selected_values: dict[str, Any]
    _filters: dict[str, Incomplete]

    def __init__(self, config: type[SearchOptions]) -> None: ...
    def add_filter(self, name: str, values: list[Incomplete]) -> None: ...
    def aggregate(self, search: Incomplete) -> Incomplete: ...
    def apply(
        self,
        identity: Identity,
        search: RecordsSearchV2,
        params: dict[str, Any],
    ) -> RecordsSearchV2: ...
    @property
    def facets(self) -> dict[str, Any]: ...
    def filter(self, search: RecordsSearchV2) -> RecordsSearchV2: ...
