from contextlib import contextmanager
from typing import IO, Any, ClassVar, Generator, Mapping, Self, TypedDict, overload
from uuid import UUID

from invenio_files_rest.models import (  # type: ignore[import-untyped]
    FileInstance,
    ObjectVersion,
)
from invenio_records.api import Record as RecordBase
from invenio_records.dumpers import Dumper
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import DictField, SystemField, SystemFieldsMixin
from invenio_records.systemfields.model import ModelField
from invenio_records_resources.records.systemfields import PIDField
from invenio_records_resources.records.transfer import TransferField

class Record(RecordBase, SystemFieldsMixin):
    send_signals: ClassVar[bool]
    enable_jsonref: ClassVar[bool]
    model_cls: ClassVar[type[RecordMetadata]]
    dumper: ClassVar[Dumper]
    metadata: ClassVar[DictField]
    pid: ClassVar[
        PIDField
    ]  # keep typing ; this is not present on the record but is used overall

class FileAccess:
    _hidden: bool
    dirty: bool

    def __init__(self, hidden: bool | None = ...) -> None: ...
    def dump(self) -> dict[str, bool]: ...
    @classmethod
    def from_dict(cls, access_dict: dict[str, bool]) -> Self: ...
    @property
    def hidden(self) -> bool: ...
    @hidden.setter
    def hidden(self, value: bool) -> None: ...

class FileAccessField(SystemField):  # type: ignore[misc]
    _access_obj_class: type[FileAccess]

    def __init__(
        self, key: str | None = ..., access_obj_class: type[FileAccess] = ...
    ) -> None: ...
    def obj(self, instance: "FileRecord") -> FileAccess: ...
    def set_obj(
        self, record: "FileRecord", obj: dict[str, bool] | FileAccess
    ) -> None: ...
    def pre_commit(self, record: "FileRecord") -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[FileRecord]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: FileRecord, owner: type[FileRecord]
    ) -> FileAccess: ...
    def __set__(self, instance: FileRecord, value: FileAccess) -> None: ...  # type: ignore[override]

class FileRecord(RecordBase, SystemFieldsMixin):
    send_signals: ClassVar[bool]
    enable_jsonref: ClassVar[bool]
    model_cls: ClassVar[type[RecordMetadata]]
    record_cls: ClassVar[type["Record"] | None]
    dumper: ClassVar[Dumper]
    metadata: ClassVar[DictField]
    access: ClassVar[FileAccessField]
    key: ClassVar[ModelField]
    object_version_id: ClassVar[ModelField]
    object_version: ClassVar[ModelField]
    record_id: ClassVar[ModelField]
    _record: ClassVar[ModelField]
    transfer: ClassVar[TransferField]

    @property
    def file(self) -> File | None: ...
    @classmethod
    def get_by_key(cls, record_id: UUID, key: str) -> Self | None: ...
    def get_stream(self, mode: str) -> IO[bytes]: ...
    @classmethod
    def list_by_record(
        cls, record_id: UUID, with_deleted: bool = ...
    ) -> Generator[Self, None, None]: ...
    @contextmanager
    def open_stream(self, mode: str) -> Generator[IO[bytes], None, None]: ...
    @property
    def record(self) -> "Record": ...
    @classmethod
    def remove_all(cls, record_id: UUID) -> None: ...

class File:
    object_model: ObjectVersion | None
    file_model: FileInstance | None

    def __getattr__(self, name: str) -> Any: ...
    def __init__(
        self,
        object_model: ObjectVersion | None = ...,
        file_model: FileInstance | None = ...,
    ) -> None: ...

    class FileDump(TypedDict, total=False):
        checksum: str
        mimetype: str
        size: int
        ext: str | None
        object_version_id: str
        file_id: str

    def dumps(self) -> FileDump: ...
    @property
    def ext(self) -> str | None: ...
    @classmethod
    def from_dump(cls, data: Mapping[str, Any]) -> Self: ...
    @property
    def key(self) -> str: ...
    @property
    def file_id(self) -> UUID: ...

class PersistentIdentifierWrapper:
    pid_value: str

    def __init__(self, pid_value: str) -> None: ...
