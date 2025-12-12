from typing import Iterable

from invenio_records.dumpers.search import SearchDumperExt

class RelationDumperExt(SearchDumperExt):
    def __init__(self, key: str, fields: Iterable[str] | None = ...) -> None: ...
