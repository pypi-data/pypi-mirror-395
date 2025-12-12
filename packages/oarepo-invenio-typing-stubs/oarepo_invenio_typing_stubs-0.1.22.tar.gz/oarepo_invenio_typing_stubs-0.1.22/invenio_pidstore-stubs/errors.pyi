"""Errors for persistent identifiers.

Type stubs for invenio_pidstore.errors.
"""

from typing import Any

class PersistentIdentifierError(Exception):
    """Base class for PIDStore errors."""

class PIDValueError(PersistentIdentifierError):
    """Base class for value errors."""

    pid_type: str
    pid_value: str

    def __init__(
        self,
        pid_type: str,
        pid_value: str,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...

class PIDDoesNotExistError(PIDValueError):
    """PID does not exists error."""

class PIDAlreadyExists(PIDValueError):
    """Persistent identifier already exists error."""

class ResolverError(PersistentIdentifierError):
    """Persistent identifier does not exists."""

    pid: Any

    def __init__(
        self,
        pid: Any,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...

class PIDDeletedError(ResolverError):
    """Persistent identifier is deleted."""

    record: Any

    def __init__(
        self,
        pid: Any,
        record: Any,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...

class PIDMissingObjectError(ResolverError):
    """Persistent identifier has no object."""

class PIDUnregistered(ResolverError):
    """Persistent identifier has not been registered."""

class PIDRedirectedError(ResolverError):
    """Persistent identifier is redirected to another pid."""

    destination_pid: Any

    def __init__(
        self,
        pid: Any,
        dest_pid: Any,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...

class PIDObjectAlreadyAssigned(PersistentIdentifierError):
    """Persistent identifier is already assigned to another object."""

class PIDInvalidAction(PersistentIdentifierError):
    """Invalid operation on persistent identifier in current state."""
