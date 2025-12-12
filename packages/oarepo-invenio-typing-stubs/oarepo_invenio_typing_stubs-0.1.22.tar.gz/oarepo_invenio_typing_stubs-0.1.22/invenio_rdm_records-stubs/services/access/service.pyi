from __future__ import annotations

from datetime import date, datetime
from typing import Any, ClassVar, Generic, TypeVar

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_drafts_resources.services.records import RecordService
from invenio_drafts_resources.services.records.config import RecordServiceConfig
from invenio_rdm_records.records.api import RDMDraft, RDMParent, RDMRecord
from invenio_rdm_records.services.decorators import groups_enabled
from invenio_rdm_records.services.result_items import (
    GrantItem,
    GrantList,
    SecretLinkItem,
    SecretLinkList,
)
from invenio_rdm_records.services.results import GrantSubjectExpandableField
from invenio_records_resources.services.records.results import RecordItem
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from invenio_records_resources.services.uow import unit_of_work

C = TypeVar("C", bound=RecordServiceConfig)

class RecordAccessService(RecordService[C], Generic[C]):
    group_subject_type: ClassVar[str]

    def link_result_item(self, *args: Any, **kwargs: Any) -> SecretLinkItem: ...
    def link_result_list(self, *args: Any, **kwargs: Any) -> SecretLinkList: ...
    def grant_result_item(self, *args: Any, **kwargs: Any) -> GrantItem: ...
    def grants_result_list(self, *args: Any, **kwargs: Any) -> GrantList: ...
    def get_parent_and_record_or_draft(
        self, _id: str
    ) -> tuple[RDMParent, RDMRecord | RDMDraft]: ...
    @property
    def schema_secret_link(self) -> ServiceSchemaWrapper: ...
    @property
    def schema_grant(self) -> ServiceSchemaWrapper: ...
    @property
    def schema_grants(self) -> ServiceSchemaWrapper: ...
    @property
    def schema_request_access(self) -> ServiceSchemaWrapper: ...
    @property
    def schema_access_settings(self) -> ServiceSchemaWrapper: ...
    @property
    def expandable_fields(self) -> list[GrantSubjectExpandableField]: ...
    def _update_parent_request(self, parent: RDMParent, uow: UnitOfWork) -> None: ...
    def _validate_secret_link_expires_at(
        self,
        expires_at: date | datetime | None,
        is_specified: bool = True,
        secret_link: Any | None = None,
    ) -> datetime | None: ...
    @unit_of_work()
    def create_secret_link(
        self,
        identity: Identity,
        id_: str,
        data: dict[str, Any],
        links_config: Any | None = None,
        uow: UnitOfWork | None = None,
    ) -> SecretLinkItem: ...
    def read_all_secret_links(
        self, identity: Identity, id_: str, links_config: Any | None = None
    ) -> SecretLinkList: ...
    def read_secret_link(
        self,
        identity: Identity,
        id_: str,
        link_id: str,
        links_config: Any | None = None,
    ) -> SecretLinkItem: ...
    @unit_of_work()
    def update_secret_link(
        self,
        identity: Identity,
        id_: str,
        link_id: str,
        data: dict[str, Any],
        links_config: Any | None = None,
        uow: UnitOfWork | None = None,
    ) -> SecretLinkItem: ...
    @unit_of_work()
    def delete_secret_link(
        self,
        identity: Identity,
        id_: str,
        link_id: str,
        links_config: Any | None = None,
        uow: UnitOfWork | None = None,
    ) -> bool: ...
    def _validate_grant_subject(self, identity: Identity, grant: Any) -> bool: ...
    @unit_of_work()
    def bulk_create_grants(
        self,
        identity: Identity,
        id_: str,
        data: dict[str, Any],
        expand: bool = False,
        uow: UnitOfWork | None = None,
    ) -> GrantList: ...
    def read_grant(
        self, identity: Identity, id_: str, grant_id: int, expand: bool = False
    ) -> GrantItem: ...
    @unit_of_work()
    def update_grant(
        self,
        identity: Identity,
        id_: str,
        grant_id: int,
        data: dict[str, Any],
        expand: bool = False,
        partial: bool = False,
        uow: UnitOfWork | None = None,
    ) -> GrantItem: ...
    def read_all_grants(
        self, identity: Identity, id_: str, expand: bool = False
    ) -> GrantList: ...
    @unit_of_work()
    def delete_grant(
        self, identity: Identity, id_: str, grant_id: int, uow: UnitOfWork | None = None
    ) -> bool: ...
    def _exists(
        self, created_by: dict[str, str], record_id: str, request_type: str
    ) -> bool: ...
    def request_access(
        self, identity: Identity, id_: str, data: dict[str, Any], expand: bool = False
    ) -> dict[str, Any] | RecordItem: ...
    @unit_of_work()
    def create_user_access_request(
        self,
        identity: Identity,
        id_: str,
        data: dict[str, Any],
        expand: bool = False,
        uow: UnitOfWork | None = None,
    ) -> RecordItem: ...
    @unit_of_work()
    def create_guest_access_request_token(
        self,
        identity: Identity,
        id_: str,
        data: dict[str, Any],
        expand: bool = False,
        uow: UnitOfWork | None = None,
    ) -> dict[str, Any]: ...
    @unit_of_work()
    def create_guest_access_request(
        self,
        identity: Identity,
        token: str,
        expand: bool = False,
        uow: UnitOfWork | None = None,
    ) -> RecordItem: ...
    @unit_of_work()
    def update_access_settings(
        self,
        identity: Identity,
        id_: str,
        data: dict[str, Any],
        uow: UnitOfWork | None = None,
    ) -> RecordItem: ...
    @groups_enabled(group_subject_type)
    def read_grant_by_subject(
        self,
        identity: Identity,
        id_: str,
        subject_id: str,
        subject_type: str,
        expand: bool = False,
    ) -> GrantItem: ...
    @groups_enabled(group_subject_type)
    def read_all_grants_by_subject(
        self, identity: Identity, id_: str, subject_type: str, expand: bool = False
    ) -> GrantList: ...
    @groups_enabled(group_subject_type)
    @unit_of_work()
    def update_grant_by_subject(
        self,
        identity: Identity,
        id_: str,
        subject_id: str,
        subject_type: str,
        data: dict[str, Any],
        expand: bool = False,
        uow: UnitOfWork | None = None,
    ) -> GrantItem: ...
    @groups_enabled(group_subject_type)
    @unit_of_work()
    def delete_grant_by_subject(
        self,
        identity: Identity,
        id_: str,
        subject_id: str,
        subject_type: str,
        uow: UnitOfWork | None = None,
    ) -> bool: ...
