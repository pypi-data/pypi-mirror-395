from typing import Any, Mapping

from flask_principal import Identity
from invenio_communities.communities.records.systemfields.deletion_status import (
    CommunityDeletionStatusEnum as CommunityDeletionStatusEnum,
)
from invenio_records_resources.services.records.params import ParamInterpreter
from invenio_search.api import RecordsSearchV2

class StatusParam(ParamInterpreter):
    def apply(
        self,
        identity: Identity,
        search: RecordsSearchV2,
        params: Mapping[str, Any],
    ) -> RecordsSearchV2: ...

class IncludeDeletedCommunitiesParam(ParamInterpreter):
    def apply(
        self,
        identity: Identity,
        search: RecordsSearchV2,
        params: Mapping[str, Any],
    ) -> RecordsSearchV2: ...
