# Invenio-Records package typing stubs
from invenio_records.api import Record as Record
from invenio_records.ext import InvenioRecords as InvenioRecords

__version__: str

# Copy of __all__ from invenio_records.__init__ to aid tools that don't
# resolve re-exports reliably (see agent instruction #13).
__all__: list[str] = [
    "InvenioRecords",
    "Record",
    "__version__",
]
