from typing import ClassVar

from invenio_records_resources.services.files.transfer.base import Transfer as Transfer
from invenio_records_resources.services.files.transfer.constants import (
    FETCH_TRANSFER_TYPE,
    LOCAL_TRANSFER_TYPE,
    MULTIPART_TRANSFER_TYPE,
    REMOTE_TRANSFER_TYPE,
)
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

class TransferStatus:
    PENDING: ClassVar[str]
    COMPLETED: ClassVar[str]
    FAILED: ClassVar[str]

__all__ = (
    "Transfer",
    "FETCH_TRANSFER_TYPE",
    "LOCAL_TRANSFER_TYPE",
    "MULTIPART_TRANSFER_TYPE",
    "REMOTE_TRANSFER_TYPE",
    "TransferStatus",
    "FetchTransfer",
    "LocalTransfer",
    "MultipartTransfer",
    "RemoteTransfer",
)
