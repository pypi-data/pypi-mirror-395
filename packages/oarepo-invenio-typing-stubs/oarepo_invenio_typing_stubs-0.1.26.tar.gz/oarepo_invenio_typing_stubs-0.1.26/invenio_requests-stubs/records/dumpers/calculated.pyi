from typing import (
    Any,
    Dict,
    Optional,
    Type,
)

from invenio_records.api import Record
from invenio_records.dumpers import SearchDumperExt

class CalculatedFieldDumperExt(SearchDumperExt):
    field: str
    property: str

    def __init__(self, field: str, prop: Optional[str] = None) -> None: ...
    def dump(self, record: Record, data: Dict[str, Any]) -> None: ...
    def load(self, data: Dict[str, Any], record_cls: Type[Record]) -> None: ...
