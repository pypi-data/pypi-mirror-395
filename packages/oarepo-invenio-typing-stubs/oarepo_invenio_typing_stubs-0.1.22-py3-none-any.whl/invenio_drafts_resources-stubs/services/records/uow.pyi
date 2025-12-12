from typing import Any, Optional, Protocol, Union

from invenio_db.uow import UnitOfWork
from invenio_drafts_resources.records.api import ParentRecord
from invenio_indexer.api import RecordIndexer  # type: ignore[import-untyped]
from invenio_records_resources.services.uow import RecordCommitOp

class _IndexerContext(Protocol):
    """Protocol for a service-like object carrying indexer context."""

    record_cls: type
    draft_cls: type
    indexer: RecordIndexer
    draft_indexer: RecordIndexer

class ParentRecordCommitOp(RecordCommitOp):
    """Parent record commit operation, bulk indexing records and drafts."""

    _indexer_context: Optional[Union[_IndexerContext, dict[str, Any]]]
    _record_cls: type
    _draft_cls: type
    _record_indexer: RecordIndexer
    _draft_indexer: RecordIndexer
    _bulk_index: bool

    def __init__(
        self,
        parent: ParentRecord,
        indexer_context: Optional[Union[_IndexerContext, dict[str, Any]]] = ...,
        bulk_index: bool = ...,
    ) -> None: ...
    def on_commit(self, uow: UnitOfWork) -> None: ...
    def on_post_commit(self, uow: UnitOfWork) -> None: ...
