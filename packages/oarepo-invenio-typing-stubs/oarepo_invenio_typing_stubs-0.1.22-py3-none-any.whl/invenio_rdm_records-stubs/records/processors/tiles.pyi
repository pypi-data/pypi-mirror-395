from __future__ import annotations

from typing import ContextManager, Protocol

from invenio_rdm_records.records.api import RDMDraft, RDMRecord
from invenio_rdm_records.records.processors.base import RecordFilesProcessor
from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.systemfields.files.manager import FilesManager
from invenio_records_resources.services.uow import TaskOp

class UOWLike(Protocol):
    def register(self, op: TaskOp) -> None: ...

class TilesProcessor(RecordFilesProcessor):
    """Processor to generate pyramidal TIFFs for eligible files."""

    @property
    def valid_exts(self) -> list[str]: ...
    def _can_process_file(
        self, file_record: FileRecord, draft: RDMDraft | None, record: RDMRecord
    ) -> bool: ...
    def unlocked_bucket(self, files: FilesManager) -> ContextManager[None]: ...
    def _cleanup(self, record: RDMRecord, uow: UOWLike | None = ...) -> None: ...
    def _process_file(
        self,
        file_record: FileRecord,
        draft: RDMDraft | None,
        record: RDMRecord,
        file_type: str,
        uow: UOWLike | None = ...,
    ) -> None: ...
    def _process(
        self, draft: RDMDraft | None, record: RDMRecord, uow: UOWLike | None = ...
    ) -> None: ...
