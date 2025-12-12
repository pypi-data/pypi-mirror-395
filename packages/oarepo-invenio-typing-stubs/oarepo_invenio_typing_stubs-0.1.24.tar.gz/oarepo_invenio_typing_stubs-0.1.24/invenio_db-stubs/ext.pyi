from typing import Any, Optional, Union

from flask.app import Flask
from flask_alembic import Alembic  # type: ignore[import-untyped]
from invenio_db.shared import SQLAlchemy  # type: ignore[import-untyped]
from sqlalchemy_continuum.manager import VersioningManager  # type: ignore[import-untyped]

class InvenioDB:
    alembic: Alembic
    versioning_manager: VersioningManager
    def __init__(self, app: Optional[Flask] = ..., **kwargs: Any): ...
    def init_app(self, app: Flask, **kwargs: Any) -> None: ...
    def init_db(
        self,
        app: Flask,
        entry_point_group: Optional[Union[str, bool]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def init_versioning(
        self,
        app: Flask,
        database: SQLAlchemy,
        versioning_manager: Optional[VersioningManager] = ...,
    ) -> None: ...
