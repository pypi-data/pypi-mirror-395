from io import (
    BufferedReader,
    BytesIO,
)
from typing import (
    Optional,
    Union,
)

from flask_principal import (
    Identity,
)
from invenio_records_resources.records.api import (
    FileRecord,
    Record,
)
from invenio_records_resources.services.files.components.base import (
    FileServiceComponent,
)
from werkzeug.wsgi import LimitedStream

class FileContentComponent(FileServiceComponent):
    def delete_file(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
        deleted_file: FileRecord,
    ): ...
    def get_file_content(
        self, identity: Identity, id_: str, file_key: str, record: Record
    ): ...
    def set_file_content(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        stream: Union[LimitedStream, BytesIO, BufferedReader],
        content_length: Optional[int],
        record: Record,
    ): ...
