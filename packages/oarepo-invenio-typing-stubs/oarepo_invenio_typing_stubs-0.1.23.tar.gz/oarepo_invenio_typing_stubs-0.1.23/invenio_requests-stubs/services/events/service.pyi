from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from _typeshed import Incomplete
from flask_principal import Identity
from invenio_db.uow import UnitOfWork, dummy_uow
from invenio_records_resources.services import RecordService
from invenio_records_resources.services.records.results import RecordItem, RecordList
from invenio_requests.customizations import CommentEventType as CommentEventType
from invenio_requests.customizations.event_types import LogEventType as LogEventType
from invenio_requests.records.api import Request, RequestEvent
from invenio_requests.records.api import RequestEventFormat as RequestEventFormat
from invenio_requests.resolvers.registry import ResolverRegistry as ResolverRegistry
from invenio_requests.services.events.config import RequestEventsServiceConfig
from invenio_requests.services.results import (
    EntityResolverExpandableField as EntityResolverExpandableField,
)

C = TypeVar("C", bound=RequestEventsServiceConfig)

class RequestEventsService(RecordService[C], Generic[C]):
    @property
    def expandable_fields(self) -> List[EntityResolverExpandableField]: ...
    def _get_creator(
        self, identity: Identity, request: Optional[Request] = ...
    ) -> Dict[str, Any]: ...
    def _get_event(
        self, event_id: Union[str, int], with_deleted: bool = ...
    ) -> RequestEvent: ...
    def _get_request(self, request_id: Union[str, int]) -> Request: ...
    def create(  # type: ignore[override]
        self,
        identity: Identity,
        request_id: Union[str, int, UUID],
        data: Dict[str, Any],
        event_type: Incomplete,
        uow: UnitOfWork = dummy_uow,
        expand: bool = False,
        notify: bool = True,
    ) -> RecordItem: ...
    def search(  # type: ignore[override]
        self,
        identity: Identity,
        request_id: Union[str, int],
        params: Optional[Dict[str, Any]] = None,
        search_preference: Optional[str] = None,
        **kwargs: Any,
    ) -> RecordList: ...
    @property
    def request_cls(self) -> Type[Request]: ...
