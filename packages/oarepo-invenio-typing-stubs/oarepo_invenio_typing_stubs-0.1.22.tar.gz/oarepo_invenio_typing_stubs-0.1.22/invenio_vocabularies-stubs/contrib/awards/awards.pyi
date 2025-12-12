from invenio_records.systemfields import MultiRelationsField as MultiRelationsField
from invenio_records_resources.factories.factory import (
    RecordTypeFactory as RecordTypeFactory,
)
from invenio_vocabularies.contrib.awards.config import (
    AwardsSearchOptions as AwardsSearchOptions,
)
from invenio_vocabularies.contrib.awards.config import (
    service_components as service_components,
)
from invenio_vocabularies.contrib.awards.schema import AwardSchema as AwardSchema
from invenio_vocabularies.contrib.awards.serializer import (
    AwardL10NItemSchema as AwardL10NItemSchema,
)
from invenio_vocabularies.contrib.funders.api import Funder as Funder
from invenio_vocabularies.contrib.subjects.api import Subject as Subject
from invenio_vocabularies.services.permissions import (
    PermissionPolicy as PermissionPolicy,
)

award_relations: MultiRelationsField
record_type: RecordTypeFactory
