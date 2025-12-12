from typing import Any, Iterable, Iterator

from flask_principal import Identity
from invenio_records_resources.services.base.results import (
    ServiceItemResult,
    ServiceListResult,
)

class SecretLinkItem(ServiceItemResult):
    _errors: list[dict[str, Any]] | None
    _identity: Identity
    _links_config: Any
    _link: Any
    _service: Any
    _data: dict[str, Any] | None
    def __init__(
        self,
        service: Any,
        identity: Identity,
        link: Any,
        errors: list[dict[str, Any]] | None = None,
        links_config: Any | None = None,
    ) -> None: ...
    @property
    def id(self) -> str: ...
    @property
    def data(self) -> dict[str, Any]: ...
    def to_dict(self) -> dict[str, Any]: ...

class SecretLinkList(ServiceListResult):
    _service: Any
    _identity: Identity
    _results: Iterable[dict[str, Any]]
    _links_config: Any
    def __init__(
        self,
        service: Any,
        identity: Identity,
        results: Iterable[dict[str, Any]],
        links_config: Any | None = None,
    ) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[dict[str, Any]]: ...
    @property
    def results(self) -> Iterator[dict[str, Any]]: ...
    def to_dict(self) -> dict[str, Any]: ...

class GrantItem(ServiceItemResult):
    _errors: list[dict[str, Any]] | None
    _identity: Identity
    _grant: Any
    _service: Any
    _expand: bool
    _fields_resolver: Any
    _data: dict[str, Any] | None
    def __init__(
        self,
        service: Any,
        identity: Identity,
        grant: Any,
        errors: list[dict[str, Any]] | None = None,
        expandable_fields: Any | None = None,
        expand: bool = False,
    ) -> None: ...
    @property
    def data(self) -> dict[str, Any]: ...
    def to_dict(self) -> dict[str, Any]: ...

class GrantList(ServiceListResult):
    _service: Any
    _identity: Identity
    _results: Iterable[dict[str, Any]]
    _fields_resolver: Any
    _expand: bool
    def __init__(
        self,
        service: Any,
        identity: Identity,
        results: Iterable[dict[str, Any]],
        expandable_fields: Any | None = None,
        expand: bool = False,
    ) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[dict[str, Any]]: ...
    @property
    def results(self) -> Iterator[dict[str, Any]]: ...
    def to_dict(self) -> dict[str, Any]: ...
