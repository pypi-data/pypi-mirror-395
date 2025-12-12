from typing import Any, Generic, Iterator, TypeVar, Union

from flask_principal import AnonymousIdentity, Identity
from invenio_records_resources.services.base.components import BaseServiceComponent
from invenio_records_resources.services.base.config import ServiceConfig
from invenio_records_resources.services.base.results import (
    ServiceBulkItemResult,
    ServiceBulkListResult,
    ServiceItemResult,
    ServiceListResult,
)

# having generic here (unlike in sources) to be able to have subclasses
# of config safely typed inside the Service
C = TypeVar("C", bound=ServiceConfig)

class Service(Generic[C]):
    config: C  # keep typing
    def __init__(self, config: C) -> None: ...
    def check_permission(
        self,
        identity: Union[Identity, AnonymousIdentity],
        action_name: str,
        **kwargs: Any,
    ) -> bool: ...
    @property
    def components(self) -> Iterator[BaseServiceComponent]: ...
    @property
    def id(self) -> str: ...
    def permission_policy(self, action_name: str, **kwargs: Any) -> Any: ...
    def require_permission(
        self,
        identity: Union[Identity, AnonymousIdentity],
        action_name: str,
        **kwargs: Any,
    ) -> None: ...
    def result_bulk_item(self, *args: Any, **kwargs: Any) -> ServiceBulkItemResult: ...
    def result_bulk_list(self, *args: Any, **kwargs: Any) -> ServiceBulkListResult: ...
    def result_item(self, *args: Any, **kwargs: Any) -> ServiceItemResult: ...
    def result_list(self, *args: Any, **kwargs: Any) -> ServiceListResult: ...
    def run_components(self, action: str, *args: Any, **kwargs: Any) -> None: ...
