from typing import TYPE_CHECKING, Any, Dict, Optional, Self, Type, Union, overload

from invenio_records.systemfields import SystemField
from invenio_requests.customizations import EventType as EventType
from invenio_requests.proxies import (
    current_event_type_registry as current_event_type_registry,
)

if TYPE_CHECKING:
    from invenio_records.models import RecordMetadataBase
    from invenio_requests.customizations.event_types import EventType
    from invenio_requests.records.api import RequestEvent

class EventTypeField(SystemField):  # type: ignore[misc]
    def _set(
        self,
        model: "RecordMetadataBase",
        value: Union[str, "EventType", Type["EventType"]],
    ): ...
    @staticmethod
    def get_instance(
        value: Union[str, "EventType", Type["EventType"]],
    ) -> "EventType": ...
    def obj(self, instance: "RequestEvent") -> "EventType": ...
    def pre_init(
        self,
        record: "RequestEvent",
        data: Dict[str, Any],
        model: Optional["RecordMetadataBase"] = None,
        **kwargs: Any,
    ) -> None: ...
    def set_obj(self, instance: "RequestEvent", obj: "EventType") -> None: ...
    @overload  # type: ignore[override]
    def __get__(self, instance: None, owner: type[RequestEvent]) -> Self: ...  # type: ignore # keep typing tighter
    @overload
    def __get__(  # type: ignore # keep typing tighter
        self, instance: RequestEvent, owner: type[RequestEvent]
    ) -> EventType: ...
    def __set__(self, instance: RequestEvent, value: EventType) -> None: ...  # type: ignore[override]
