from invenio_db.shared import SQLAlchemy

current_db: SQLAlchemy  # intentionally not using a LocalProxy[SQLAlchemy] here as mypy does not understand it
