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

class FileProcessorComponent(FileServiceComponent):
    def commit_file(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
    ): ...
    def extract_file_metadata(
        self,
        identity: Identity,
        id_: str,
        file_key: str,
        record: Record,
        file_record: FileRecord,
    ): ...
