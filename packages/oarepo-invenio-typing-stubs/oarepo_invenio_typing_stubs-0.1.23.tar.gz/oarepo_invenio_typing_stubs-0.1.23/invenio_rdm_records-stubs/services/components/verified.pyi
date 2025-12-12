from typing import Any

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.records.api import RDMDraft, RDMRecord

class BaseHandler:
    def update_draft(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMDraft | None = ...,
        errors: Any | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def delete_draft(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMDraft | None = ...,
        force: bool = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def edit(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def new_version(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def publish(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def post_publish(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        is_published: bool = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...

class UserModerationHandler(BaseHandler):
    @property
    def enabled(self) -> bool: ...
    def run(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        uow: UnitOfWork | None = ...,
    ) -> None: ...
    def publish(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...

class ContentModerationComponent(ServiceComponent):
    def update_draft(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMDraft | None = ...,
        errors: Any | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def delete_draft(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMDraft | None = ...,
        force: bool = ...,
        **kwargs: Any,
    ) -> None: ...
    def edit(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def publish(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def post_publish(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        is_published: bool = ...,
        **kwargs: Any,
    ) -> None: ...
    def new_version(
        self,
        identity: Identity,
        draft: RDMDraft | None = ...,
        record: RDMRecord | None = ...,
        **kwargs: Any,
    ) -> None: ...
