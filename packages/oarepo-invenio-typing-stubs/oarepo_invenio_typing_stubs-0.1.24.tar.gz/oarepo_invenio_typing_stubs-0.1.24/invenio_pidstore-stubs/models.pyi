"""Persistent identifier store and registration.

Type stubs for invenio_pidstore.models.
"""

import logging
import uuid
from enum import Enum
from typing import ClassVar, Optional, Union

from flask_babel import LazyString
from sqlalchemy import Column, Index
from sqlalchemy_utils.models import Timestamp

PID_STATUS_TITLES: dict[str, LazyString]
logger: logging.Logger

class PIDStatus(Enum):
    """Constants for possible status of any given PID."""

    NEW = "N"
    RESERVED = "K"
    REGISTERED = "R"
    REDIRECTED = "M"
    DELETED = "D"

    def __init__(self, value: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __str__(self) -> str: ...
    @property
    def title(self) -> str: ...

class _Model: ...

class PersistentIdentifier(_Model, Timestamp):
    """Store and register persistent identifiers."""

    __tablename__: ClassVar[str]
    __table_args__: ClassVar[tuple[Index, ...]]

    id: Column[int]
    pid_type: Column[str]
    pid_value: Column[str]
    pid_provider: Column[Optional[str]]
    status: Column[PIDStatus]
    object_type: Column[Optional[str]]
    object_uuid: Column[Optional[uuid.UUID]]

    @classmethod
    def create(
        cls,
        pid_type: str,
        pid_value: str,
        pid_provider: Optional[str] = None,
        status: PIDStatus = ...,
        object_type: Optional[str] = None,
        object_uuid: Optional[Union[str, uuid.UUID]] = None,
    ) -> PersistentIdentifier: ...
    @classmethod
    def get(
        cls,
        pid_type: str,
        pid_value: Union[str, int],
        pid_provider: Optional[str] = None,
    ) -> PersistentIdentifier: ...
    @classmethod
    def get_by_object(
        cls,
        pid_type: str,
        object_type: str,
        object_uuid: Union[str, uuid.UUID],
    ) -> PersistentIdentifier: ...
    def has_object(self) -> bool: ...
    def get_assigned_object(
        self, object_type: Optional[str] = None
    ) -> Optional[uuid.UUID]: ...
    def assign(
        self,
        object_type: str,
        object_uuid: Union[str, uuid.UUID],
        overwrite: bool = False,
    ) -> bool: ...
    def unassign(self) -> bool: ...
    def get_redirect(self) -> PersistentIdentifier: ...
    def redirect(self, pid: PersistentIdentifier) -> bool: ...
    def reserve(self) -> bool: ...
    def register(self) -> bool: ...
    def delete(self) -> bool: ...
    def sync_status(self, status: PIDStatus) -> bool: ...
    def is_redirected(self) -> bool: ...
    def is_registered(self) -> bool: ...
    def is_deleted(self) -> bool: ...
    def is_new(self) -> bool: ...
    def is_reserved(self) -> bool: ...
    def __repr__(self) -> str: ...

class Redirect(_Model, Timestamp):
    """Redirect for a persistent identifier."""

    __tablename__: ClassVar[str]

    id: Column[uuid.UUID]
    pid_id: Column[int]
    pid: PersistentIdentifier

class RecordIdentifier(_Model):
    """Sequence generator for integer record identifiers."""

    __tablename__: ClassVar[str]

    recid: Column[int]

    @classmethod
    def next(cls) -> int: ...
    @classmethod
    def max(cls) -> int: ...
    @classmethod
    def _set_sequence(cls, val: int) -> None: ...
    @classmethod
    def insert(cls, val: int) -> None: ...

__all__ = (
    "PersistentIdentifier",
    "PIDStatus",
    "RecordIdentifier",
    "Redirect",
)
