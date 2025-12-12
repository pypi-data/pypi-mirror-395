from typing import TYPE_CHECKING, Any, Dict, List, Optional

from flask_principal import Identity
from invenio_db.uow import UnitOfWork, dummy_uow
from invenio_records_resources.records.api import Record as BaseRecord
from invenio_records_resources.services.records.components import (
    DataComponent,
    ServiceComponent,
)
from invenio_requests.customizations.event_types import (
    ReviewersUpdatedType as ReviewersUpdatedType,
)
from invenio_requests.proxies import current_events_service as current_events_service

if TYPE_CHECKING:
    from invenio_requests.records.api import Request

class RequestNumberComponent(ServiceComponent):
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional["Request"] = None,
        **kwargs: Any,
    ) -> None: ...

class EntityReferencesComponent(ServiceComponent):
    def create(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: Optional["Request"] = None,
        **kwargs: Any,
    ) -> None: ...

class RequestDataComponent(DataComponent):
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: BaseRecord | None = None,
        **kwargs: Any,
    ) -> None: ...

class RequestReviewersComponent(ServiceComponent):
    def _ensure_no_duplicates(self, reviewers: List[Any]) -> List[Any]: ...
    def _reviewers_updated(
        self, previous_reviewers: List[Any], new_reviewers: List[Any]
    ) -> bool: ...
    def _validate_reviewers(self, reviewers: List[Any]) -> None: ...
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: BaseRecord | None = None,
        uow: UnitOfWork = dummy_uow,
        **kwargs: Any,
    ) -> None: ...

class RequestPayloadComponent(DataComponent):
    def update(
        self,
        identity: Identity,
        data: Optional[Dict[str, Any]] = None,
        record: BaseRecord | None = None,
        **kwargs: Any,
    ) -> None: ...
