from abc import ABC
from io import BufferedReader, BytesIO
from typing import Any, ClassVar

from flask_principal import (
    Identity,
)
from invenio_db.uow import UnitOfWork
from invenio_records_resources.records.api import (
    FileRecord,
    Record,
)
from invenio_records_resources.services.files.schema import BaseTransferSchema
from invenio_records_resources.services.files.service import FileService
from werkzeug.wrappers import Response
from werkzeug.wsgi import LimitedStream

class TransferStatus:
    """Transfer status constants."""

    PENDING: ClassVar[str]
    COMPLETED: ClassVar[str]
    FAILED: ClassVar[str]

class Transfer(ABC):
    transfer_type: ClassVar[str]
    Schema: ClassVar[type[BaseTransferSchema]]
    # Instance attributes set in __init__
    record: Record
    key: str
    file_service: FileService | None
    _file_record: FileRecord | None
    uow: UnitOfWork | None
    def __init__(
        self,
        record: Record,
        key: str,
        file_service: FileService | None,
        file_record: FileRecord | None = ...,
        uow: UnitOfWork | None = ...,
    ): ...
    def commit_file(self) -> None: ...
    def delete_file(self) -> None: ...
    def expand_links(self, identity: Identity, self_url: str) -> dict[str, Any]: ...
    @property
    def file_record(self) -> FileRecord: ...
    def init_file(
        self,
        record: Record,
        file_metadata: dict[str, Any],
        **kwargs,
    ) -> FileRecord: ...
    def send_file(self, *, restricted: bool, as_attachment: bool) -> Response: ...
    def set_file_content(
        self,
        stream: BytesIO | BufferedReader | LimitedStream,
        content_length: int | None,
    ) -> None: ...
    @property
    def status(self) -> str: ...

__all__ = (
    "TransferStatus",
    "Transfer",
)
