from typing import Self, overload

from invenio_records.systemfields import SystemField
from invenio_requests.customizations import RequestType as RequestType
from invenio_requests.proxies import (
    current_request_type_registry as current_request_type_registry,
)
from invenio_requests.records.api import Request

class RequestTypeField(SystemField):  # type: ignore[misc]
    def __init__(self, key: str = "type") -> None: ...
    def obj(self, instance: "Request") -> "RequestType": ...
    def set_obj(self, instance: "Request", obj: "RequestType") -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Request]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Request, owner: type[Request]
    ) -> RequestType: ...
    def __set__(self, instance: Request, value: RequestType) -> None: ...  # type: ignore[override]
