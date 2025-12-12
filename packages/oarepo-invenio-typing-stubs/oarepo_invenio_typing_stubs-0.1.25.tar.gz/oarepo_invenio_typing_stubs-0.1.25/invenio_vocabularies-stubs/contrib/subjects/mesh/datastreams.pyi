from typing import Any

from invenio_vocabularies.datastreams.transformers import (
    BaseTransformer as BaseTransformer,
)
from invenio_vocabularies.datastreams.transformers import (
    TransformerError as TransformerError,
)

class MeshSubjectsTransformer(BaseTransformer):
    def apply(self, stream_entry, *args, **kwargs): ...

VOCABULARIES_DATASTREAM_READERS: dict[str, type[Any]]
VOCABULARIES_DATASTREAM_WRITERS: dict[str, type[Any]]
VOCABULARIES_DATASTREAM_TRANSFORMERS: dict[str, type[MeshSubjectsTransformer]]
