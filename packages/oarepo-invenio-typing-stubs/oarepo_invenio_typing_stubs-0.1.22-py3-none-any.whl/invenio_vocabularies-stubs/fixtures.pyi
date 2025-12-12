from collections.abc import Generator
from typing import Any

from invenio_vocabularies.datastreams.factories import (
    DataStreamFactory as DataStreamFactory,
)
from invenio_vocabularies.proxies import current_service as current_service

class VocabularyFixture:
    _filepath: str
    def __init__(self, filepath: str, delay: bool = True) -> None: ...
    def _load_vocabulary(
        self, config: dict[str, Any], delay: bool = True, **kwargs
    ) -> list[Any]: ...
    def _create_vocabulary(self, id_: str, pid_type: str, *args, **kwargs) -> Any: ...
    def load(self, *args, **kwargs) -> Generator[list[Any], None, None]: ...
