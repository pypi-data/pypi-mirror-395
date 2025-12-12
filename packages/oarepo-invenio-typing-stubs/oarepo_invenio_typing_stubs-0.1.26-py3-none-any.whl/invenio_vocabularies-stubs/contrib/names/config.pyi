from typing import Any, Dict, Mapping, Type

from invenio_records_resources.services import SearchOptions
from invenio_records_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.records.queryparser import QueryParser
from invenio_vocabularies.contrib.names.components import (
    InternalIDComponent as InternalIDComponent,
)
from invenio_vocabularies.services.components import PIDComponent as PIDComponent

names_schemes: Dict[
    str, Dict[str, Any]
]  # intentionally not using a LocalProxy[Dict[str, Dict[str, Any]]] here as mypy does not understand it

class NamesSearchOptions(SearchOptions):
    # NOTE: expose immutable defaults so overrides replace rather than mutate.
    suggest_parser_cls: type[QueryParser] | None
    sort_default: str
    sort_default_no_query: str
    sort_options: Mapping[str, Mapping[str, Any]]

service_components: tuple[Type[ServiceComponent], ...]
