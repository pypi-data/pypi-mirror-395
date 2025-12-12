"""DataCite PID provider.

Type stubs for invenio_pidstore.providers.datacite.
"""

from typing import Any, ClassVar, Optional

from datacite import DataCiteMDSClient
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_pidstore.providers.base import BaseProvider

class DataCiteProvider(BaseProvider):
    """DOI provider using DataCite API."""

    pid_type: ClassVar[str]  # type: ignore[assignment]
    pid_provider: ClassVar[str]  # type: ignore[assignment]
    default_status: ClassVar[PIDStatus]
    api: DataCiteMDSClient

    def __init__(
        self,
        pid: PersistentIdentifier,
        client: Optional[DataCiteMDSClient] = None,
        **kwargs: Any,
    ) -> None: ...
    def reserve(self, doc: str) -> bool: ...
    def register(self, url: str, doc: str) -> bool: ...
    def update(self, url: str, doc: str) -> bool: ...
    def delete(self) -> bool: ...
    def sync_status(self) -> bool: ...
