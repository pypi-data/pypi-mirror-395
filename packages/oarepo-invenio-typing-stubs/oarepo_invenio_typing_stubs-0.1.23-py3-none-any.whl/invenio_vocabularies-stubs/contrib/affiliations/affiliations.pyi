from invenio_records_resources.factories.factory import (
    RecordTypeFactory as RecordTypeFactory,
)
from invenio_vocabularies.contrib.affiliations.config import (
    AffiliationsSearchOptions as AffiliationsSearchOptions,
)
from invenio_vocabularies.contrib.affiliations.config import (
    service_components as service_components,
)
from invenio_vocabularies.contrib.affiliations.schema import (
    AffiliationSchema as AffiliationSchema,
)
from invenio_vocabularies.services.permissions import (
    PermissionPolicy as PermissionPolicy,
)

record_type: RecordTypeFactory
