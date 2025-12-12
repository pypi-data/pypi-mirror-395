from __future__ import annotations

from typing import Optional, Tuple

import marshmallow as ma
from _typeshed import Incomplete
from invenio_records_resources.records.api import Record
from invenio_records_resources.services.base import Service

class BaseRecordSchema(ma.Schema):
    def clean(
        self, input_data: dict[str, Incomplete], **kwargs
    ) -> dict[str, Incomplete]: ...

class BaseGhostSchema(ma.Schema): ...

class ServiceSchemaWrapper:
    def __init__(
        self,
        service: Service,
        schema: type[ma.Schema],
    ): ...
    def _build_context(
        self, base_context: dict[str, Incomplete]
    ) -> dict[str, Incomplete]: ...
    def dump(
        self,
        data: Record,
        schema_args: None = ...,
        context: Optional[dict[str, Incomplete]] = ...,
    ) -> dict[str, Incomplete]: ...
    def load(
        self,
        data: dict[str, Incomplete],
        schema_args: None = ...,
        context: Optional[dict[str, Incomplete]] = ...,
        raise_errors: bool = ...,
    ) -> Tuple[dict[str, Incomplete], list[dict[str, Incomplete]]]: ...
