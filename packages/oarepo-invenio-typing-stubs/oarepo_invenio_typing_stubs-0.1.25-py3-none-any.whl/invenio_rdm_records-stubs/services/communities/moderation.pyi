from typing import Any

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_rdm_records.records.api import RDMRecord
from invenio_records_resources.services.records.components import ServiceComponent

class BaseHandler:
    def create(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        data: dict[str, Any] | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        data: dict[str, Any] | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def delete(
        self,
        identity: Identity,
        data: dict[str, Any] | None = ...,
        record: RDMRecord | None = ...,
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
    def create(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        data: dict[str, Any] | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        data: dict[str, Any] | None = ...,
        uow: UnitOfWork | None = ...,
        **kwargs: Any,
    ) -> None: ...

class ContentModerationComponent(ServiceComponent):
    def create(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        data: dict[str, Any] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        data: dict[str, Any] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def delete(
        self,
        identity: Identity,
        record: RDMRecord | None = ...,
        data: dict[str, Any] | None = ...,
        **kwargs: Any,
    ) -> None: ...
