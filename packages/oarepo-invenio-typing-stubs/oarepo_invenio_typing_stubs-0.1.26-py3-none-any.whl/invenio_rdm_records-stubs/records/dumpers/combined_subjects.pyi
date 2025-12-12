from typing import Any

from invenio_records.dumpers import SearchDumperExt

SPLITCHAR: str

class CombinedSubjectsDumperExt(SearchDumperExt):
    _splitchar: str
    def __init__(self, splitchar: str = ...) -> None: ...
    def dump(self, record: Any, data: dict[str, Any]) -> None: ...
    def load(self, data: dict[str, Any], record_cls: type) -> None: ...
