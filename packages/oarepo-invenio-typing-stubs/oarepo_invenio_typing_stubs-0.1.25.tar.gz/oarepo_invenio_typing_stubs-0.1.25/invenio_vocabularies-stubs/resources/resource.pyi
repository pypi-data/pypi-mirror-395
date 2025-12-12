from typing import Any, Dict, Generic, List, Tuple, TypeVar

from flask_resources import BaseListSchema as BaseListSchema
from flask_resources import JSONSerializer as JSONSerializer
from flask_resources import MarshmallowSerializer as MarshmallowSerializer
from flask_resources import ResponseHandler as ResponseHandler
from invenio_access.permissions import system_identity as system_identity
from invenio_records_resources.resources import RecordResource
from invenio_records_resources.resources import (
    RecordResourceConfig as RecordResourceConfig,
)
from invenio_records_resources.resources import (
    SearchRequestArgsSchema as SearchRequestArgsSchema,
)
from invenio_records_resources.resources.records.headers import (
    etag_headers as etag_headers,
)
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_headers,
    request_search_args,
    request_view_args,
)
from invenio_vocabularies.resources.config import VocabulariesResourceConfig
from invenio_vocabularies.resources.serializer import (
    VocabularyL10NItemSchema as VocabularyL10NItemSchema,
)
from invenio_vocabularies.services.service import VocabulariesService
from marshmallow import fields as fields

C = TypeVar("C", bound=VocabulariesResourceConfig)
S = TypeVar("S", bound=VocabulariesService)

class VocabulariesResource(RecordResource[C, S], Generic[C, S]):
    def create_url_rules(self) -> List[Any]: ...
    @request_search_args
    @request_view_args
    def search(self) -> Tuple[Dict[str, Any], int]: ...
    @request_view_args
    @request_data
    def create(self) -> Tuple[Dict[str, Any], int]: ...
    @request_view_args
    def read(self) -> Tuple[Dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    @request_data
    def update(self) -> Tuple[Dict[str, Any], int]: ...
    @request_headers
    @request_view_args
    def delete(self) -> Tuple[str, int]: ...
    @request_data
    def launch(self) -> Tuple[str, int]: ...

class VocabulariesAdminResource(RecordResource[C, S], Generic[C, S]):
    def create_url_rules(self) -> List[Any]: ...
    @request_search_args
    def search(self) -> Tuple[Dict[str, Any], int]: ...
