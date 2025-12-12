from typing import Callable

from invenio_records_resources.services.records.facets import (
    CombinedTermsFacet,
    NestedTermsFacet,
    TermsFacet,
)


access_status: TermsFacet
is_published: TermsFacet
filetype: TermsFacet
language: TermsFacet
resource_type: NestedTermsFacet
subject_nested: NestedTermsFacet
subject: TermsFacet


def deprecated_subject_nested() -> NestedTermsFacet: ...


def get_subject_schemes() -> list[str]: ...


subject_combined: CombinedTermsFacet
