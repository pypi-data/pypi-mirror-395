"""Module that mints, stores, registers and resolves persistent identifiers.

Type stubs for invenio_pidstore package.
"""

from invenio_pidstore.ext import InvenioPIDStore as InvenioPIDStore
from invenio_pidstore.proxies import current_pidstore as current_pidstore

__version__: str

# Workaround for tools that don't see reexports: copy __all__ from source
__all__ = ("__version__", "InvenioPIDStore", "current_pidstore")
