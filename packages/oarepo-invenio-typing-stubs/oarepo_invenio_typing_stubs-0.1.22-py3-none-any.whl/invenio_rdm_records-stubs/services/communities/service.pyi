from typing import Any, Dict, Generic, List, Tuple, TypeVar

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_rdm_records.services.config import RDMRecordCommunitiesConfig
from invenio_records_resources.services import RecordIndexerMixin, Service
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper

C = TypeVar("C", bound=RDMRecordCommunitiesConfig)

class RecordCommunitiesService(Service[C], RecordIndexerMixin, Generic[C]):
    @property
    def schema(self) -> ServiceSchemaWrapper: ...
    @property
    def communities_schema(self) -> ServiceSchemaWrapper: ...
    @property
    def record_cls(self): ...
    @property
    def draft_cls(self): ...
    def _exists(self, community_id: str, record: Any) -> str | None: ...
    def _include(
        self,
        identity: Identity,
        community_id: str,
        comment: str | None,
        require_review: bool,
        record: Any,
        uow: UnitOfWork,
    ): ...
    def add(
        self, identity: Identity, id_: str, data: Dict[str, Any], uow: UnitOfWork
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: ...
    def _remove(self, identity: Identity, community_id: str, record: Any) -> None: ...
    def remove(
        self, identity: Identity, id_: str, data: Dict[str, Any], uow: UnitOfWork
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: ...
    def search(
        self,
        identity: Identity,
        id_: str,
        params: Dict[str, Any] | None = ...,
        search_preference: str | None = ...,
        expand: bool = ...,
        extra_filter: Any | None = ...,
        **kwargs: Any,
    ): ...
    def _get_excluded_communities_filter(
        self, record: Any, identity: Identity, id_: str
    ): ...
    def search_suggested_communities(
        self,
        identity: Identity,
        id_: str,
        params: Dict[str, Any] | None = ...,
        search_preference: str | None = ...,
        expand: bool = ...,
        by_membership: bool = ...,
        extra_filter: Any | None = ...,
        **kwargs: Any,
    ): ...
    def set_default(
        self, identity: Identity, id_: str, data: Dict[str, Any], uow: UnitOfWork
    ): ...
    def bulk_add(
        self,
        identity: Identity,
        community_id: str,
        record_ids: List[str],
        set_default: bool = ...,
        uow: UnitOfWork | None = None,
    ) -> List[Dict[str, Any]]: ...
