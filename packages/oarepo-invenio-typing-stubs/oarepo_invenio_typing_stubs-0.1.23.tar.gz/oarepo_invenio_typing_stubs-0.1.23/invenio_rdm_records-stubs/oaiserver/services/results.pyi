from typing import Any, Iterator

from flask_principal import Identity
from invenio_records_resources.services.base.results import (
    ServiceItemResult,
    ServiceListResult,
)

class BaseServiceItemResult(ServiceItemResult):
    _identity: Identity
    _item: Any
    _schema: Any
    _links_tpl: Any
    _data: dict[str, Any] | None

    @property
    def links(self) -> dict[str, Any]: ...
    @property
    def data(self) -> dict[str, Any]: ...
    def to_dict(self) -> dict[str, Any]: ...

class BaseServiceListResult(ServiceListResult):
    _identity: Identity
    _results: Any
    _service: Any
    _schema: Any
    _params: dict[str, Any] | None
    _links_tpl: Any
    _links_item_tpl: Any

    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[dict[str, Any]]: ...
    @property
    def total(self) -> int: ...
    @property
    def hits(self) -> Iterator[dict[str, Any]]: ...
    @property
    def pagination(self) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...

class OAISetItem(BaseServiceItemResult): ...
class OAISetList(BaseServiceListResult): ...
class OAIMetadataFormatItem(BaseServiceItemResult): ...
class OAIMetadataFormatList(BaseServiceListResult): ...
