from typing import Optional, Self, overload

from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields.calculated import CalculatedField
from invenio_requests.customizations.states import RequestState

class RequestStateCalculatedField(CalculatedField):
    def __init__(
        self, key: Optional[str] = None, expected_state: RequestState = ...
    ) -> None: ...
    def calculate(self, record: Record) -> bool: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: Record, owner: type[Record]
    ) -> bool: ...
    def __set__(self, instance: Record, value: bool) -> None: ...  # type: ignore[override]
