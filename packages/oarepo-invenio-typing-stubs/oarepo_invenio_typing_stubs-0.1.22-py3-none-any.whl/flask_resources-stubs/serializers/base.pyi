from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from marshmallow import Schema

class BaseSerializer:
    def serialize_object(self, obj: Any) -> Any: ...
    def serialize_object_list(self, obj_list: Any) -> Any: ...

class MarshmallowSerializer(BaseSerializer):
    schema_context: dict[str, Any]
    format_serializer: BaseSerializer
    object_schema: Schema
    list_schema: Schema | None

    def __init__(
        self,
        format_serializer_cls: type[BaseSerializer],
        object_schema_cls: type[Schema],
        list_schema_cls: type[Schema] | None = ...,
        schema_context: dict[str, Any] | None = ...,
        schema_kwargs: dict[str, Any] | None = ...,
        **serializer_options: Any,
    ) -> None: ...
    def dump_obj(self, obj: Any) -> Any: ...
    def dump_list(self, obj_list: Any) -> Any: ...

class DumperMixin:
    def post_dump(
        self, data: Any, original: Any | None = ..., **kwargs: Any
    ) -> Any: ...
    def pre_dump(self, data: Any, original: Any | None = ..., **kwargs: Any) -> Any: ...

class BaseSerializerSchema(Schema):
    dumpers: list[DumperMixin]

    def __init__(
        self, dumpers: Iterable[DumperMixin] | None = ..., **kwargs: Any
    ) -> None: ...
    def post_dump_pipeline(
        self, data: Any, original: Any, many: bool, **kwargs: Any
    ) -> Any: ...
    def pre_dump_pipeline(self, data: Any, many: bool, **kwargs: Any) -> Any: ...

__all__ = (
    "BaseSerializer",
    "MarshmallowSerializer",
    "DumperMixin",
    "BaseSerializerSchema",
)
