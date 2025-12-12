from __future__ import annotations

from typing import Mapping

from _typeshed import Incomplete
from invenio_records_resources.services.records.params import (
    ParamInterpreter as ParamInterpreter,
)

class FilterParam(ParamInterpreter):
    param_name: str
    field_name: str
    def __init__(
        self, param_name: str, field_name: str, config: Incomplete
    ) -> None: ...
    @classmethod
    def factory(
        cls, param: str | None = None, field: str | None = None
    ) -> Incomplete: ...
    def apply(
        self, identity: Incomplete, search: Incomplete, params: Mapping[str, Incomplete]
    ) -> Incomplete: ...
