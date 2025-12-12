from typing import Any, Dict

from invenio_access.permissions import system_identity as system_identity
from invenio_vocabularies.datastreams.writers import ServiceWriter as ServiceWriter

class SubjectsServiceWriter(ServiceWriter):
    def __init__(self, *args, **kwargs) -> None: ...
    def _entry_id(self, entry): ...

VOCABULARIES_DATASTREAM_READERS: dict[str, Any]
VOCABULARIES_DATASTREAM_TRANSFORMERS: dict[str, Any]
VOCABULARIES_DATASTREAM_WRITERS: dict[str, type[SubjectsServiceWriter] | Any]
DATASTREAM_CONFIG: Dict[str, list[dict[str, str]]]
