from typing import Any, Dict, Type

from invenio_vocabularies.contrib.common.ror.datastreams import (
    RORTransformer as RORTransformer,
)
from invenio_vocabularies.datastreams.writers import ServiceWriter as ServiceWriter

class FundersServiceWriter(ServiceWriter):
    def __init__(self, *args, **kwargs) -> None: ...
    def _entry_id(self, entry): ...

class FundersRORTransformer(RORTransformer):
    def __init__(
        self, *args, vocab_schemes=None, funder_fundref_doi_prefix=None, **kwargs
    ) -> None: ...

VOCABULARIES_DATASTREAM_READERS: Dict[str, Type[Any]]
VOCABULARIES_DATASTREAM_WRITERS: Dict[str, Type[FundersServiceWriter]]
VOCABULARIES_DATASTREAM_TRANSFORMERS: Dict[str, Type[FundersRORTransformer]]
DATASTREAM_CONFIG: Dict[str, Any]
