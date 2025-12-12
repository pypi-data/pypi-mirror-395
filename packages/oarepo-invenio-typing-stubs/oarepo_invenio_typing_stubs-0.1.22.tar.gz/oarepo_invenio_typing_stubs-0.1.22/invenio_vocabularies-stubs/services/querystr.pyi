from typing import Any, Optional

from flask_principal import Identity
from invenio_records_resources.services.records.params import SuggestQueryParser
from invenio_search.engine import dsl

class FilteredSuggestQueryParser(SuggestQueryParser):
    filter_field: Optional[str]
    def __init__(
        self,
        identity: Optional[Identity] = None,
        filter_field: Optional[str] = None,
        extra_params: Optional[dict[str, Any]] = None,
    ) -> None: ...
    def parse(self, query_str: str) -> dsl.query.Query: ...
    def extract_subtype_s(self, query_str: str) -> tuple[list[str], str]: ...
