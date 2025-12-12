"""Define PIDStore proxies.

Type stubs for invenio_pidstore.proxies.
"""

from invenio_pidstore.ext import _PIDStoreState

current_pidstore: _PIDStoreState  # intentionally not using a LocalProxy[_PIDStoreState] here as mypy does not understand it
