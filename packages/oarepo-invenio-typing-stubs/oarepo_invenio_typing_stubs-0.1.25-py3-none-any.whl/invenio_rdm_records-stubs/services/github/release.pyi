from __future__ import annotations

from typing import Any

from flask_principal import Identity
from invenio_db.uow import UnitOfWork
from invenio_github.api import GitHubRelease

class RDMGithubRelease(GitHubRelease):
    metadata_cls: type[Any]
    @property
    def metadata(self) -> dict[str, Any]: ...
    def get_custom_fields(self) -> dict[str, Any]: ...
    def get_owner(self) -> dict[str, Any] | None: ...
    def _upload_files_to_draft(
        self, identity: Identity, draft: Any, uow: UnitOfWork
    ) -> None: ...
