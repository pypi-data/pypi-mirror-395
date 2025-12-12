from typing import Any, ClassVar, Dict

from flask.wrappers import Response
from invenio_records_resources.records.api import (
    FileRecord,
    Record,
)
from invenio_records_resources.services.files.schema import BaseTransferSchema
from invenio_records_resources.services.files.transfer.base import Transfer

class RemoteTransferBase(Transfer):
    class Schema(BaseTransferSchema):
        def validate_names(self, value: str) -> None: ...

class RemoteTransfer(RemoteTransferBase):
    transfer_type: ClassVar[str]
    def init_file(
        self, record: Record, file_metadata: Dict[str, Any], **kwargs
    ) -> FileRecord: ...
    def send_file(self, *, as_attachment: bool, **kwargs: Any) -> Response: ...
    @property
    def status(self) -> str: ...
