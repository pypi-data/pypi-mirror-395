from typing import Any

from invenio_records.systemfields import SystemFieldContext

class CommunitiesFieldContext(SystemFieldContext):
    def query_by_community(self, community_or_id: Any): ...
