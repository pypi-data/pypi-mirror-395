from io import (
    BufferedReader,
    BytesIO,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from flask_principal import (
    AnonymousIdentity,
    Identity,
)
from invenio_records_resources.records.api import (
    FileRecord,
    Record,
)
from invenio_records_resources.services.base.components import BaseServiceComponent
from werkzeug.wsgi import LimitedStream

class FileServiceComponent(BaseServiceComponent):
    def commit_file(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
    ): ...
    def delete_all_files(
        self, identity: Identity, id_: str, record: Record, results: List[Any]
    ): ...
    def delete_file(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
        deleted_file: FileRecord,
    ): ...
    def extract_file_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
        file_record: FileRecord,
    ): ...
    def get_file_content(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
    ): ...
    def init_files(
        self,
        identity: Identity,
        id_: str,
        record: Record,
        data: List[Dict[str, Any]],
    ): ...
    def list_files(
        self,
        identity: Identity,
        id_: str,
        record: Record,
    ): ...
    def read_file_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
    ): ...
    def set_file_content(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        stream: Union[BytesIO, BufferedReader, LimitedStream],
        content_length: Optional[int],
        record: Record,
    ): ...
    def update_file_metadata(
        self,
        identity: AnonymousIdentity,
        id_: str,
        file_key: str,
        record: Record,
        data: Dict[str, Dict[str, str]],
    ): ...
    def get_file_transfer_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
        transfer_metadata: Dict[str, Any],
    ): ...
    def update_file_transfer_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
        transfer_metadata: Dict[str, Any],
    ): ...
