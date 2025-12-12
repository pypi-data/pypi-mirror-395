from typing import Any

from invenio_vocabularies.contrib.subjects.config import (
    euroscivoc_file_url as euroscivoc_file_url,
)
from invenio_vocabularies.datastreams.transformers import (
    RDFTransformer as RDFTransformer,
)

class EuroSciVocSubjectsTransformer(RDFTransformer): ...

VOCABULARIES_DATASTREAM_TRANSFORMERS: dict[str, type[EuroSciVocSubjectsTransformer]]
DATASTREAM_CONFIG: dict[str, Any]
