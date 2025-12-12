from invenio_records_resources.factories.factory import (
    RecordTypeFactory as RecordTypeFactory,
)
from invenio_vocabularies.contrib.subjects.config import (
    SubjectsSearchOptions as SubjectsSearchOptions,
)
from invenio_vocabularies.contrib.subjects.config import (
    service_components as service_components,
)
from invenio_vocabularies.contrib.subjects.schema import SubjectSchema as SubjectSchema
from invenio_vocabularies.records.pidprovider import (
    PIDProviderFactory as PIDProviderFactory,
)
from invenio_vocabularies.records.systemfields import (
    BaseVocabularyPIDFieldContext as BaseVocabularyPIDFieldContext,
)
from invenio_vocabularies.services.permissions import (
    PermissionPolicy as PermissionPolicy,
)

record_type: RecordTypeFactory
