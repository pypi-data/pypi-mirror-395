from collections.abc import Mapping
from typing import Any, Generic, TypeVar

from invenio_records_resources.resources.records.config import RecordResourceConfig
from invenio_records_resources.resources.records.resource import (
    RecordResource,
    request_view_args,
)
from invenio_vocabularies.contrib.names.services import NamesService
from marshmallow import fields

class NamesResourceConfig(RecordResourceConfig):
    # NOTE: configs expose immutable defaults so subclasses override instead of
    # mutating shared state.
    routes: Mapping[str, str]
    request_view_args: Mapping[str, fields.Field]

C = TypeVar("C", bound=NamesResourceConfig)
S = TypeVar("S", bound=NamesService)

class NamesResource(RecordResource[C, S], Generic[C, S]):
    def create_url_rules(self) -> list[Any]: ...
    @request_view_args
    def name_resolve_by_id(self): ...
