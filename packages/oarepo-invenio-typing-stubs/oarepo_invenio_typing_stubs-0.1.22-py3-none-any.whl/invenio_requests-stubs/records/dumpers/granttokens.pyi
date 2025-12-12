from typing import (
    Any,
    Dict,
    Tuple,
    Type,
)

from invenio_records.api import Record
from invenio_records.dumpers import SearchDumperExt

class GrantTokensDumperExt(SearchDumperExt):
    grants_field: str
    fields: Tuple[str, ...]

    def __init__(self, *fields: str) -> None: ...
    def dump(self, record: Record, data: Dict[str, Any]) -> None: ...
    def load(self, data: Dict[str, Any], record_cls: Type[Record]) -> None: ...
