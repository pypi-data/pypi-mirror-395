from typing import Any

from invenio_vocabularies.datastreams.factories import (
    DataStreamFactory as DataStreamFactory,
)

def process_datastream(config: dict[str, Any]) -> None: ...
