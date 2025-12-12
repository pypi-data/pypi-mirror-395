from typing import Any

from invenio_vocabularies.contrib.funders.config import (
    FundersSearchOptions as FundersSearchOptions,
)
from invenio_vocabularies.contrib.funders.config import (
    service_components as service_components,
)
from invenio_vocabularies.contrib.funders.schema import FunderSchema as FunderSchema
from invenio_vocabularies.contrib.funders.serializer import (
    FunderL10NItemSchema as FunderL10NItemSchema,
)
from invenio_vocabularies.services.permissions import (
    PermissionPolicy as PermissionPolicy,
)

record_type: Any
