from collections.abc import Iterator, Mapping
from typing import Any

from invenio_records_resources.records.api import FileRecord
from marshmallow import Schema
from marshmallow_oneofschema.one_of_schema import OneOfSchema

class BaseTransferSchema(Schema):
    class Meta:
        unknown: Any

class TransferTypeSchemas(Mapping[str, Schema | type[Schema]]):
    def __getitem__(self, transfer_type: str) -> Schema | type[Schema]: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...

class TransferSchema(OneOfSchema):
    type_field: str
    type_field_remove: bool
    # Follow OneOfSchema contract: Mapping[str, Schema | type[Schema]]
    type_schemas: Mapping[str, Schema | type[Schema]]
    def get_obj_type(
        self,
        obj: Any,
    ) -> str: ...

class FileAccessSchema(Schema):
    class Meta:
        unknown: Any

class FileSchema(Schema):
    class Meta:
        unknown: Any

    def dump_file_fields(
        self, obj: dict[str, Any], original: FileRecord, **kwargs: Any
    ) -> dict[str, Any]: ...
    def dump_status(self, obj: FileRecord) -> str: ...

class InitFileSchemaMixin(Schema):
    class Meta:
        unknown: Any

    def _fill_initial_transfer(self, data: Any, **kwargs: Any) -> Any: ...
