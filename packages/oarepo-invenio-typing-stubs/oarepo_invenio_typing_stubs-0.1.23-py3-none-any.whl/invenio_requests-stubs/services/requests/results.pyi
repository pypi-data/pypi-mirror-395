from collections.abc import Generator
from typing import Any, Dict, Iterator, List, Optional

from flask_principal import Identity
from invenio_records_resources.services.records.results import RecordItem, RecordList
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from invenio_requests.records.api import Request
from invenio_requests.services.requests.links import RequestLinksTemplate
from invenio_requests.services.requests.service import RequestsService

class RequestItem(RecordItem):
    def __init__(
        self,
        service: RequestsService,
        identity: Identity,
        request: Request,
        errors: Optional[List[Dict[str, Any]]] = None,
        links_tpl: Optional[RequestLinksTemplate] = None,
        schema: Optional[ServiceSchemaWrapper] = None,
        expandable_fields: Optional[List[Any]] = None,
        expand: bool = False,
    ) -> None: ...
    @property
    def _obj(self) -> Request: ...
    @property
    def id(self) -> str: ...
    def __getitem__(self, key: str) -> Any: ...
    @property
    def links(self) -> Dict[str, Any]: ...
    @property
    def links_tpl(self) -> RequestLinksTemplate: ...
    @links_tpl.setter
    def links_tpl(self, links_tpl: RequestLinksTemplate) -> None: ...
    @property
    def data(self) -> Dict[str, Any]: ...
    @property
    def errors(self) -> List[Dict[str, Any]]: ...
    def to_dict(self) -> Dict[str, Any]: ...
    def has_permissions_to(self, actions: List[str]) -> Dict[str, bool]: ...

class RequestList(RecordList):
    def __init__(
        self,
        service: RequestsService,
        identity: Identity,
        results: Iterator[Any],
        params: Optional[Dict[str, Any]] = None,
        links_tpl: Optional[Any] = None,
        links_item_tpl: Optional[RequestLinksTemplate] = None,
        expandable_fields: Optional[List[Any]] = None,
        expand: bool = False,
    ) -> None: ...
    @property
    def hits(self) -> Generator[Dict[str, Any], None, None]: ...
    def to_dict(self) -> Dict[str, Any]: ...
