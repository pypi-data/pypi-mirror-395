"""Record ID provider.

Type stubs for invenio_pidstore.providers.recordid.
"""

from typing import ClassVar

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.base import BaseProvider

class RecordIdProvider(BaseProvider):
    """Record identifier provider."""

    pid_type: ClassVar[str]  # type: ignore[assignment]
    pid_provider: ClassVar[None]  # type: ignore[assignment]
    default_status: ClassVar[PIDStatus]
