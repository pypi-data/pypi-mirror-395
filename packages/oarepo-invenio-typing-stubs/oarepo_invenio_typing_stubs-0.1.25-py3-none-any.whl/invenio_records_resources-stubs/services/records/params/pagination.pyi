from __future__ import annotations

from typing import Mapping

from _typeshed import Incomplete
from invenio_records_resources.services.records.params.base import ParamInterpreter

class PaginationParam(ParamInterpreter):
    def apply(
        self,
        identity: Incomplete,
        search: Incomplete,
        params: Mapping[str, Incomplete],
    ) -> Incomplete: ...
