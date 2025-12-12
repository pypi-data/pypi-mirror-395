from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import Mapped
from sqlalchemy.orm.mapper import Mapper

class Timestamp:
    created: Mapped[datetime]
    updated: Mapped[datetime]

def timestamp_before_update(
    mapper: Mapper, connection: Connection, target: Any
) -> None: ...

class _Model: ...

class RecordMetadataBase(_Model, Timestamp):
    encoder: Optional[Any]
    id: Mapped[UUID]
    json: Mapped[Optional[Dict[str, Any]]]
    version_id: Mapped[int]
    __mapper_args__: Dict[str, Any]

    def __init__(self, data: Optional[Dict[str, Any]] = ..., **kwargs: Any) -> None: ...
    @property
    def is_deleted(self) -> Any: ...
    @is_deleted.setter
    def is_deleted(self, value: bool) -> None: ...
    @property
    def data(self) -> Dict[str, Any]: ...
    @data.setter
    def data(self, value: Dict[str, Any]) -> None: ...
    @classmethod
    def encode(cls, value: Dict[str, Any]) -> Dict[str, Any]: ...
    @classmethod
    def decode(cls, json: Any) -> Any: ...

class RecordMetadata(RecordMetadataBase):
    __tablename__: str
    __versioned__: Dict[str, Any]
