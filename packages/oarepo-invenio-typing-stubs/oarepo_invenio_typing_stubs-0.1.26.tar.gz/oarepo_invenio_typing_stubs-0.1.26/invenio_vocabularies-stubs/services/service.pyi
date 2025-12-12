from typing import Any, Dict, Generic, List, Optional, TypeVar

from flask_principal import Identity
from invenio_db.uow import UnitOfWork, dummy_uow
from invenio_records_resources.services import RecordService
from invenio_records_resources.services.records.results import RecordList
from invenio_search.engine import dsl
from invenio_vocabularies.records.models import VocabularyType as VocabularyType
from invenio_vocabularies.services.config import (
    VocabulariesServiceConfig,
    VocabularyTypesServiceConfig,
)
from invenio_vocabularies.services.tasks import process_datastream as process_datastream

CTypeConfig = TypeVar("CTypeConfig", bound=VocabularyTypesServiceConfig)

class VocabularyTypeService(RecordService[CTypeConfig], Generic[CTypeConfig]):
    def rebuild_index(
        self, identity: Identity, uow: UnitOfWork = dummy_uow
    ) -> bool: ...
    def search(
        self,
        identity: Identity,
        params: Optional[Dict[str, Any]] = ...,
        search_preference: Optional[str] = ...,
        expand: bool = ...,
        **kwargs,
    ) -> RecordList: ...

CVocabConfig = TypeVar("CVocabConfig", bound=VocabulariesServiceConfig)

class VocabulariesService(RecordService[CVocabConfig], Generic[CVocabConfig]):
    @property
    def task_schema(self): ...
    def create_type(
        self,
        identity: Identity,
        id: str,
        pid_type: str,
        uow: UnitOfWork = dummy_uow,
    ) -> VocabularyType: ...
    def read_all(  # type: ignore[override]
        self,
        identity: Identity,
        fields: List[str],
        type: str,
        cache: bool = True,
        extra_filter: dsl.query.Query | str = "",
        **kwargs,
    ) -> RecordList: ...
    def read_many(
        self,
        identity: Identity,
        ids: List[str],
        fields: List[str] | None = None,
        **kwargs: Any,
    ) -> RecordList: ...
    def search(
        self,
        identity: Identity,
        params: Optional[Dict[str, Any]] = ...,
        search_preference: Optional[str] = ...,
        expand: bool = ...,
        **kwargs: Any,
    ) -> RecordList: ...
    def launch(self, identity: Identity, data: Dict[str, Any]) -> bool: ...
