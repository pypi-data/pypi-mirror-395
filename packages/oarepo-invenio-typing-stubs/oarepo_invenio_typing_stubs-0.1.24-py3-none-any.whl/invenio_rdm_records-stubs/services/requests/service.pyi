from __future__ import annotations

from typing import Any, Generic, TypeVar

from flask_principal import Identity
from invenio_rdm_records.services.config import RDMRecordRequestsConfig
from invenio_records_resources.services import Service
from invenio_records_resources.services.records.results import RecordList

C = TypeVar("C", bound=RDMRecordRequestsConfig)

class RecordRequestsService(Service[C], Generic[C]):
    @property
    def record_cls(self) -> Any: ...
    def search(
        self,
        identity: Identity,
        record_pid: str,
        params: dict[str, Any] | None = ...,
        search_preference: str | None = ...,
        expand: bool = ...,
        extra_filter: Any | None = ...,
        **kwargs: Any,
    ) -> RecordList: ...
