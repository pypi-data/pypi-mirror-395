from typing import Self, overload

from invenio_records.systemfields import SystemField
from invenio_requests.records.api import Request

class RequestStatusField(SystemField):  # type: ignore[misc]
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Request]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Request, owner: type[Request]
    ) -> str: ...
    def __set__(self, instance: Request, value: str) -> None: ...  # type: ignore[override]
