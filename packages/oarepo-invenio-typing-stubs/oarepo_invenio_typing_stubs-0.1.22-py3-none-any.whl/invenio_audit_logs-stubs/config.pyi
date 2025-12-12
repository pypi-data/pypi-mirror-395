from typing import Any, Dict, List

from invenio_records_resources.services.records.facets import TermsFacet as TermsFacet

# NOTE: Facets config follows the common pattern used across Invenio packages.

AUDIT_LOGS_SEARCH: Dict[str, List[str]]
AUDIT_LOGS_FACETS: Dict[
    str, Dict[str, Any]
]  # {"facet": TermsFacet, "ui": {"field": str}}
AUDIT_LOGS_SORT_OPTIONS: Dict[
    str, Dict[str, Any]
]  # {"title": str, "fields": List[str]}
AUDIT_LOGS_ENABLED: bool
AUDIT_LOGS_METADATA_FIELDS: Dict[str, bool]
