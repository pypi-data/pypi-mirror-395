from typing import Any

from invenio_records.dumpers import SearchDumperExt

class PIDsDumperExt(SearchDumperExt):
    def dump(self, record: Any, data: dict[str, Any]) -> None: ...
    def load(self, data: dict[str, Any], record_cls: type) -> None: ...
