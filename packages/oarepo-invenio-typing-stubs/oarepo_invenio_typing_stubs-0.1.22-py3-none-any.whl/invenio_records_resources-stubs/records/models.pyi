from typing import Any, ClassVar

from invenio_files_rest.models import ObjectVersion
from invenio_records.models import RecordMetadataBase
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.schema import Column

class FileRecordModelMixin:
    __record_model_cls__: ClassVar[type[RecordMetadataBase] | None]
    key: Column[str]

    @declared_attr
    def record_id(cls) -> Column[Any]: ...
    @declared_attr
    def record(cls) -> Relationship[RecordMetadataBase]: ...
    @declared_attr
    def object_version_id(cls) -> Column[Any]: ...
    @declared_attr
    def object_version(cls) -> Relationship[ObjectVersion]: ...
    @declared_attr
    def __table_args__(cls) -> Any: ...
