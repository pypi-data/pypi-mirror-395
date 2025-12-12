"""Record identifier provider V2.

Type stubs for invenio_pidstore.providers.recordid_v2.
"""

from typing import Any, ClassVar, Dict, Optional

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.base import BaseProvider

class RecordIdProviderV2(BaseProvider):
    """Record identifier provider V2."""

    pid_type: ClassVar[str]  # type: ignore[assignment]
    pid_provider: ClassVar[None]  # type: ignore[assignment]
    default_status_with_obj: ClassVar[PIDStatus]
    default_status: ClassVar[PIDStatus]

    @classmethod
    def generate_id(cls, options: Optional[Dict[str, Any]] = None) -> str: ...
