from typing import Any, Callable, Dict, List, Mapping, Optional, Union

from flask_principal import (
    Identity,
)
from invenio_records_resources.pagination import Pagination
from invenio_records_resources.records.api import FileRecord, Record
from invenio_records_resources.services.files.links import FileEndpointLink
from invenio_records_resources.services.records.links import (
    RecordEndpointLink,
    RecordLink,
)

def preprocess_vars(vars: Dict[str, Any]) -> Dict[str, Any]: ...

class EndpointLink:
    def __init__(
        self,
        endpoint: str,
        when: Optional[Callable] = ...,
        vars: Optional[Callable] = ...,
        params: Optional[List[str]] = ...,
    ): ...
    def expand(
        self,
        obj: Union[Record, FileRecord, Pagination, Any],
        context: Dict[str, Any],
    ) -> str: ...
    def should_render(
        self,
        obj: Union[Record, FileRecord, Pagination, Any],
        context: Dict[str, Any],
    ) -> bool: ...
    @staticmethod
    def vars(obj: Any, vars: Dict[str, Any]) -> None: ...

class ExternalLink:
    def __init__(
        self,
        uritemplate: str,
        when: Optional[Callable] = ...,
        vars: Optional[Callable] = ...,
    ): ...

class Link:
    def __init__(self, *args, **kwargs): ...

class LinksTemplate:
    def __init__(
        self,
        links: (
            Mapping[
                str,
                RecordLink
                | Link
                | RecordEndpointLink
                | FileEndpointLink
                | EndpointLink,
            ]
            | None
        ) = ...,
        context: Any = ...,
    ): ...
    @property
    def context(
        self,
    ) -> Dict[str, Any]: ...
    def expand(
        self,
        identity: Identity,
        obj: Union[Record, FileRecord, Pagination, Any],
    ) -> Dict[str, str]: ...

class ConditionalLink:
    def __init__(
        self,
        cond: Optional[Callable] = None,
        if_: Optional[
            Link | EndpointLink
        ] = None,  # keep typing as there are two different link classes
        else_: Optional[Link | EndpointLink] = None,
    ): ...
    def should_render(
        self, obj: Union[Record, FileRecord, Pagination, Any], ctx: Dict[str, Any]
    ) -> bool: ...
    def expand(
        self, obj: Union[Record, FileRecord, Pagination, Any], ctx: Dict[str, Any]
    ) -> str: ...

class NestedLinks:
    def __init__(
        self,
        links: Dict[
            str,
            Union[RecordLink, Link, RecordEndpointLink, FileEndpointLink, EndpointLink],
        ],
        key: str | None = None,
        load_key: str | None = None,
        dump_key: str | None = None,
        context_func: Any | None = None,
    ): ...
    def context(
        self, identity: Identity, record: Record, key: str, value: Any
    ) -> Dict[str, Any]: ...
    def expand(
        self, identity: Identity, record: Record, data: Dict[str, Any]
    ) -> Any: ...
