from io import BufferedReader, BytesIO
from typing import Any, Generic, TypeVar

from flask_principal import (
    Identity,
)
from invenio_db.uow import UnitOfWork
from invenio_records_resources.records.api import Record
from invenio_records_resources.services.base.links import LinksTemplate
from invenio_records_resources.services.base.service import Service
from invenio_records_resources.services.files.config import FileServiceConfig
from invenio_records_resources.services.files.results import (
    FileItem,
    FileList,
)
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from werkzeug.wsgi import LimitedStream

C = TypeVar("C", bound=FileServiceConfig)

class FileService(Service[C], Generic[C]):
    def _get_record(
        self,
        id_: str,
        identity: Identity,
        action: str,
        file_key: str | None = ...,
    ) -> Record: ...
    def check_permission(
        self, identity: Identity, action_name: str, **kwargs
    ) -> bool: ...
    def commit_file(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        uow: UnitOfWork | None = ...,
    ) -> FileItem: ...
    def delete_all_files(
        self, identity: Identity, id_: str, uow: UnitOfWork | None = ...
    ) -> FileList: ...
    def delete_file(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        uow: UnitOfWork | None = ...,
    ) -> FileItem: ...
    def extract_file_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        uow: UnitOfWork | None = ...,
    ) -> FileItem: ...
    def file_links_item_tpl(self, id_: str) -> LinksTemplate: ...
    def file_links_list_tpl(self, id_: str) -> LinksTemplate: ...
    def file_result_item(self, *args, **kwargs) -> FileItem: ...
    def file_result_list(self, *args, **kwargs) -> FileList: ...
    @property
    def file_schema(self) -> ServiceSchemaWrapper: ...
    def get_file_content(
        self, identity: Identity, id_: str, file_key: str
    ) -> FileItem: ...
    def get_transfer_metadata(
        self, identity: Identity, id_: str, file_key: str
    ) -> dict[str, Any]: ...
    def init_files(
        self,
        identity: Identity,
        id_: str,
        data: list[dict[str, Any]],
        uow: UnitOfWork | None = ...,
    ) -> FileList: ...
    @property
    def initial_file_schema(self) -> ServiceSchemaWrapper: ...
    def list_files(self, identity: Identity, id_: str) -> FileList: ...
    def read_file_metadata(
        self, identity: Identity, id_: str, file_key: str
    ) -> FileItem: ...
    @property
    def record_cls(self) -> type[Record]: ...
    def set_file_content(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        stream: BytesIO | BufferedReader | LimitedStream,
        content_length: int | None = ...,
        uow: UnitOfWork | None = ...,
    ) -> FileItem: ...
    def set_multipart_file_content(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        part: int,
        stream: BytesIO | LimitedStream,
        content_length: int | None = ...,
        uow: UnitOfWork | None = ...,
    ) -> FileItem: ...
    def update_file_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        data: dict[str, Any],
        uow: UnitOfWork | None = ...,
    ) -> FileItem: ...
    def update_transfer_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        transfer_metadata: dict[str, Any],
        uow: UnitOfWork | None = ...,
    ) -> None: ...
