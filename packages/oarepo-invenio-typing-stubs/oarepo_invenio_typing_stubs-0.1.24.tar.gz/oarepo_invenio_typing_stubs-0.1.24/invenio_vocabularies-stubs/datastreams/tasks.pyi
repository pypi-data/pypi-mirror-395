from typing import Any

from invenio_vocabularies.datastreams import StreamEntry as StreamEntry
from invenio_vocabularies.datastreams.factories import WriterFactory as WriterFactory

def write_entry(writer_config: dict[str, Any], entry: Any) -> None: ...
def write_many_entry(writer_config: dict[str, Any], entries: list[Any]) -> None: ...
