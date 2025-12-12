from collections.abc import KeysView
from typing import Type, Union

from invenio_db.uow import UnitOfWork
from invenio_records_resources.records.api import FileRecord, Record
from invenio_records_resources.services.files.service import FileService
from invenio_records_resources.services.files.transfer.base import Transfer
from invenio_records_resources.services.files.transfer.providers.fetch import (
    FetchTransfer,
)
from invenio_records_resources.services.files.transfer.providers.local import (
    LocalTransfer,
)
from invenio_records_resources.services.files.transfer.providers.multipart import (
    MultipartTransfer,
)
from invenio_records_resources.services.files.transfer.providers.remote import (
    RemoteTransfer,
)

class TransferRegistry:
    _transfers: dict[str, Type[Transfer]]
    _default_transfer_type: str
    def __init__(self, default_transfer_type: str): ...
    @property
    def default_transfer_type(self) -> str: ...
    def get_transfer(
        self,
        *,
        record: Record,
        file_service: FileService,
        key: str | None = ...,
        transfer_type: str | None = ...,
        file_record: FileRecord | None = ...,
        uow: UnitOfWork | None = ...,
    ) -> Union[MultipartTransfer, RemoteTransfer, LocalTransfer, FetchTransfer]: ...
    def get_transfer_class(self, transfer_type: str) -> Union[
        Type[RemoteTransfer],
        Type[FetchTransfer],
        Type[LocalTransfer],
        Type[MultipartTransfer],
    ]: ...
    def get_transfer_types(self) -> KeysView[str]: ...
    def register(
        self,
        transfer_cls: Union[
            Type[RemoteTransfer],
            Type[FetchTransfer],
            Type[LocalTransfer],
            Type[MultipartTransfer],
        ],
    ) -> None: ...
