from __future__ import annotations

from invenio_pidstore.models import PersistentIdentifier

def retrieve_recid_by_uuid(rec_uuid) -> PersistentIdentifier: ...
