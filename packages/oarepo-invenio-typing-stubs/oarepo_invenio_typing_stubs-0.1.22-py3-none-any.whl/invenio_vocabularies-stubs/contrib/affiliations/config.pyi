from typing import Any, Dict, Mapping, Type

from invenio_records_resources.services import SearchOptions
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.records.queryparser import QueryParser
from invenio_vocabularies.services.components import PIDComponent as PIDComponent

affiliation_schemes: Dict[
    str, Dict[str, Any]
]  # intentionally not using a LocalProxy[Dict[str, Dict[str, Any]]] here as mypy does not understand it
affiliation_edmo_country_mappings: Dict[
    str, str
]  # intentionally not using a LocalProxy[Dict[str, str]] here as mypy does not understand it
localized_title: (
    str  # intentionally not using a LocalProxy[str] here as mypy does not understand it
)

class AffiliationsSearchOptions(SearchOptions):
    # NOTE: immutable defaults ensure subclasses override instead of mutating.
    suggest_parser_cls: type[QueryParser] | None
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]

service_components: tuple[Type[ServiceComponent], ...]
