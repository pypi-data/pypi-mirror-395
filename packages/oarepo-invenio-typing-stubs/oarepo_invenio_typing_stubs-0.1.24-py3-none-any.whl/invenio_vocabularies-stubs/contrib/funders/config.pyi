from typing import Any, Dict, Mapping, Type

from invenio_records_resources.services import SearchOptions
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.records.queryparser import QueryParser
from invenio_vocabularies.services.components import (
    ModelPIDComponent as ModelPIDComponent,
)

funder_schemes: Dict[
    str, Dict[str, Any]
]  # intentionally not using a LocalProxy[Dict[str, Dict[str, Any]]] here as mypy does not understand it
funder_fundref_doi_prefix: (
    str  # intentionally not using a LocalProxy[str] here as mypy does not understand it
)
localized_title: (
    str  # intentionally not using a LocalProxy[str] here as mypy does not understand it
)

class FundersSearchOptions(SearchOptions):
    # NOTE: immutable defaults ensure overrides replace rather than mutate.
    suggest_parser_cls: type[QueryParser] | None
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]

service_components: tuple[Type[ServiceComponent], ...]
