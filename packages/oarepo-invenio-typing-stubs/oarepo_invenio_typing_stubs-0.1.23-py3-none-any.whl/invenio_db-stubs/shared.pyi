from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import URL

NAMING_CONVENTION: dict[str, str]
metadata: MetaData

class SQLAlchemy(FlaskSQLAlchemy):
    Model: Any

    def apply_driver_hacks(
        self, app: Flask, sa_url: URL, options: dict[str, Any]
    ) -> tuple[URL, dict[str, Any]]: ...

def do_sqlite_connect(dbapi_connection: Any, connection_record: Any) -> None: ...
def do_sqlite_begin(dbapi_connection: Any) -> None: ...

db: SQLAlchemy
