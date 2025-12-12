"""Persistent identifier minters.

Type stubs for invenio_pidstore.minters.
"""

import uuid
from typing import Any, Dict

from invenio_pidstore.models import PersistentIdentifier

def recid_minter_v2(
    record_uuid: uuid.UUID, data: Dict[str, Any]
) -> PersistentIdentifier: ...
def recid_minter(
    record_uuid: uuid.UUID, data: Dict[str, Any]
) -> PersistentIdentifier: ...
