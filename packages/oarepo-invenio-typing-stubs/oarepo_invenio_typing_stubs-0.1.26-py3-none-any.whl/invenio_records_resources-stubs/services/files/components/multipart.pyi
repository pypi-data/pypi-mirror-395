from io import BytesIO
from typing import Union

from flask_principal import (
    Identity,
)
from invenio_records_resources.records.api import Record
from invenio_records_resources.services.files.components.base import (
    FileServiceComponent,
)
from werkzeug.wsgi import LimitedStream

class FileMultipartContentComponent(FileServiceComponent):
    def set_multipart_file_content(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        part: int,
        stream: Union[LimitedStream, BytesIO],
        content_length: int,
        record: Record,
    ): ...
