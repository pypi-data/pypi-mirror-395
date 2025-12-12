from typing import Any, Mapping

from flask_principal import Identity
from invenio_records_resources.services.records.params.sort import SortParam
from invenio_search.api import RecordsSearchV2

class CommunitiesSortParam(SortParam):
    def apply(
        self,
        identity: Identity,
        search: RecordsSearchV2,
        params: Mapping[str, Any],
    ) -> RecordsSearchV2: ...
