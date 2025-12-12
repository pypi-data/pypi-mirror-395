import abc
from abc import ABC, abstractmethod
from typing import Any

from invenio_vocabularies.datastreams.datastreams import StreamEntry as StreamEntry
from invenio_vocabularies.datastreams.errors import WriterError as WriterError
from invenio_vocabularies.datastreams.tasks import write_entry as write_entry
from invenio_vocabularies.datastreams.tasks import write_many_entry as write_many_entry

class BaseWriter(ABC, metaclass=abc.ABCMeta):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def write(
        self, stream_entry: StreamEntry, *args: Any, **kwargs: Any
    ) -> StreamEntry: ...
    @abstractmethod
    def write_many(
        self, stream_entries: list[StreamEntry], *args: Any, **kwargs: Any
    ) -> list[StreamEntry]: ...

class ServiceWriter(BaseWriter):
    def __init__(
        self,
        service_or_name,
        *args,
        identity=None,
        insert: bool = True,
        update: bool = False,
        **kwargs,
    ) -> None: ...
    def write(self, stream_entry: StreamEntry, *args, **kwargs) -> StreamEntry: ...
    def write_many(
        self, stream_entries: list[StreamEntry], *args, **kwargs
    ) -> list[StreamEntry]: ...

class YamlWriter(BaseWriter):
    def __init__(self, filepath: str, *args: Any, **kwargs: Any) -> None: ...
    def write(
        self, stream_entry: StreamEntry, *args: Any, **kwargs: Any
    ) -> StreamEntry: ...
    def write_many(
        self, stream_entries: list[StreamEntry], *args: Any, **kwargs: Any
    ) -> list[StreamEntry]: ...

class AsyncWriter(BaseWriter):
    def __init__(self, writer: BaseWriter, *args: Any, **kwargs: Any) -> None: ...
    def write(
        self, stream_entry: StreamEntry, *args: Any, **kwargs: Any
    ) -> StreamEntry: ...
    def write_many(
        self, stream_entries: list[StreamEntry], *args: Any, **kwargs: Any
    ) -> list[StreamEntry]: ...
