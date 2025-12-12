"""Module storing implementations of PID providers.

Type stubs for invenio_pidstore.providers.base.
"""

import uuid
from typing import Any, ClassVar, Optional, Self, Union

from invenio_pidstore.models import PersistentIdentifier, PIDStatus

class BaseProvider:
    """Abstract class for persistent identifier provider classes."""

    pid_type: ClassVar[Optional[str]]
    pid_provider: ClassVar[Optional[str]]
    default_status: ClassVar[PIDStatus]
    pid: PersistentIdentifier

    @classmethod
    def create(
        cls,
        pid_type: Optional[str] = None,
        pid_value: Optional[str] = None,
        object_type: Optional[str] = None,
        object_uuid: Optional[Union[str, uuid.UUID]] = None,
        status: Optional[PIDStatus] = None,
        **kwargs: Any,
    ) -> Self: ...
    @classmethod
    def get(
        cls,
        pid_value: str,
        pid_type: Optional[str] = None,
        **kwargs: Any,
    ) -> BaseProvider: ...
    def __init__(self, pid: PersistentIdentifier, **kwargs: Any) -> None: ...
    def reserve(self, *args: Any, **kwargs: Any) -> bool: ...
    def register(self, *args: Any, **kwargs: Any) -> bool: ...
    def update(self, *args: Any, **kwargs: Any) -> bool: ...
    def delete(self) -> bool: ...
    def sync_status(self) -> bool: ...
