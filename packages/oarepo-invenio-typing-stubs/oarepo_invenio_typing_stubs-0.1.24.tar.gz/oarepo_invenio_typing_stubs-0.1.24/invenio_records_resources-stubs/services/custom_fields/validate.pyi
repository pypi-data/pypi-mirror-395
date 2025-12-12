from typing import List, Optional, Set

from invenio_records_resources.services.custom_fields.base import BaseCF

def validate_custom_fields(
    available_fields: List[BaseCF],
    namespaces: Optional[Set[str]] = ...,
    given_fields: Optional[List[str]] = ...,
) -> None: ...
