import io
from collections.abc import Generator
from typing import Any

from invenio_vocabularies.datastreams.errors import ReaderError as ReaderError
from invenio_vocabularies.datastreams.errors import TransformerError as TransformerError
from invenio_vocabularies.datastreams.readers import BaseReader as BaseReader
from invenio_vocabularies.datastreams.transformers import (
    BaseTransformer as BaseTransformer,
)

class RORHTTPReader(BaseReader):
    def __init__(
        self,
        origin: str | None = None,
        mode: str = "r",
        since: str | None = None,
        *args,
        **kwargs,
    ) -> None: ...
    def read(self, item=None, *args, **kwargs) -> Generator[io.BytesIO, None, None]: ...

VOCABULARIES_DATASTREAM_READERS: dict[str, type[RORHTTPReader]]

class RORTransformer(BaseTransformer):
    vocab_schemes: dict[str, Any] | None
    funder_fundref_doi_prefix: str | None
    def __init__(
        self, *args, vocab_schemes=None, funder_fundref_doi_prefix=None, **kwargs
    ) -> None: ...
    def apply(self, stream_entry, **kwargs): ...

VOCABULARIES_DATASTREAM_TRANSFORMERS: dict[str, type[RORTransformer]]
VOCABULARIES_DATASTREAM_WRITERS: dict[str, Any]
