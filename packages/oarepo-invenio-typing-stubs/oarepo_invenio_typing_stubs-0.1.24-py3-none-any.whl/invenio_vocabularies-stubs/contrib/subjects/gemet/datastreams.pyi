from typing import Any

from invenio_vocabularies.contrib.subjects.config import (
    gemet_file_url as gemet_file_url,
)
from invenio_vocabularies.datastreams.transformers import (
    RDFTransformer as RDFTransformer,
)

class GEMETSubjectsTransformer(RDFTransformer): ...

VOCABULARIES_DATASTREAM_TRANSFORMERS: dict[str, type[GEMETSubjectsTransformer]]
DATASTREAM_CONFIG: dict[str, Any]
