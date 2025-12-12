from functools import partial
from typing import Any, Dict, Mapping

from flask_principal import Identity
from invenio_records_resources.services.records.params import (
    FilterParam,
    ParamInterpreter,
)
from invenio_requests.resolvers.registry import ResolverRegistry as ResolverRegistry
from invenio_search.api import RecordsSearchV2
from opensearch_dsl.query import Bool

class ReferenceFilterParam(FilterParam):
    def __init__(
        self, param_name: str, field_name: str, config: Dict[str, Any]
    ) -> None: ...
    def _is_valid(self, ref_type: str, ref_id: str) -> bool: ...
    def apply(
        self, identity: Identity, search: RecordsSearchV2, params: Mapping[str, Any]
    ) -> RecordsSearchV2: ...

class IsOpenParam(ParamInterpreter):
    field_name: str
    def __init__(self, field_name: str, config: Dict[str, Any]) -> None: ...
    @classmethod
    def factory(cls, field: str) -> partial: ...
    def apply(
        self, identity: Identity, search: RecordsSearchV2, params: Mapping[str, Any]
    ) -> RecordsSearchV2: ...

class SharedOrMyRequestsParam(ParamInterpreter):
    def _generate_my_requests_query(self, identity: Identity) -> Bool: ...
    def apply(
        self, identity: Identity, search: RecordsSearchV2, params: Mapping[str, Any]
    ) -> RecordsSearchV2: ...
