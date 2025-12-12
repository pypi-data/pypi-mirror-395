from typing import Any, Dict, Mapping, Type

from invenio_records_resources.services import SearchOptions
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.records.queryparser import QueryParser
from invenio_vocabularies.services.components import PIDComponent as PIDComponent

subject_schemes: Dict[
    str, Dict[str, Any]
]  # intentionally not using a LocalProxy[Dict[str, Dict[str, Any]]] here as mypy does not understand it
localized_title: (
    str  # intentionally not using a LocalProxy[str] here as mypy does not understand it
)
gemet_file_url: (
    str  # intentionally not using a LocalProxy[str] here as mypy does not understand it
)
euroscivoc_file_url: (
    str  # intentionally not using a LocalProxy[str] here as mypy does not understand it
)
nvs_file_url: (
    str  # intentionally not using a LocalProxy[str] here as mypy does not understand it
)

class SubjectsSearchOptions(SearchOptions):
    # NOTE: immutable annotations prevent shared mutable defaults.
    suggest_parser_cls: type[QueryParser] | None
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]

service_components: tuple[Type[ServiceComponent], ...]
