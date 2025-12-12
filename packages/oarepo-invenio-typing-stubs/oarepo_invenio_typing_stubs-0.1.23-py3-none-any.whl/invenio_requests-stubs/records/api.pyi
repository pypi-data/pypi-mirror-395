from enum import Enum
from typing import Any, Callable, ClassVar

from invenio_records.dumpers import Dumper
from invenio_records.models import RecordMetadata
from invenio_records.systemfields import ConstantField, DictField, ModelField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.entity_reference import (
    MultiReferenceEntityField as MultiReferenceEntityField,
)
from invenio_records_resources.records.systemfields.entity_reference import (
    ReferencedEntityField as ReferencedEntityField,
)
from invenio_requests.records.dumpers import (
    CalculatedFieldDumperExt as CalculatedFieldDumperExt,
)
from invenio_requests.records.dumpers import (
    GrantTokensDumperExt as GrantTokensDumperExt,
)
from invenio_requests.records.models import RequestEventModel as RequestEventModel
from invenio_requests.records.models import RequestMetadata as RequestMetadata
from invenio_requests.records.systemfields import EventTypeField as EventTypeField
from invenio_requests.records.systemfields import (
    ExpiredStateCalculatedField as ExpiredStateCalculatedField,
)
from invenio_requests.records.systemfields import IdentityField as IdentityField
from invenio_requests.records.systemfields import (
    RequestStateCalculatedField as RequestStateCalculatedField,
)
from invenio_requests.records.systemfields import (
    RequestStatusField as RequestStatusField,
)
from invenio_requests.records.systemfields import RequestTypeField as RequestTypeField
from invenio_requests.records.systemfields.entity_reference import (
    check_allowed_creators as check_allowed_creators,
)
from invenio_requests.records.systemfields.entity_reference import (
    check_allowed_receivers as check_allowed_receivers,
)
from invenio_requests.records.systemfields.entity_reference import (
    check_allowed_reviewers as check_allowed_reviewers,
)
from invenio_requests.records.systemfields.entity_reference import (
    check_allowed_topics as check_allowed_topics,
)

class Request(Record):
    model_cls: ClassVar[type[RecordMetadata]]
    dumper: ClassVar[Dumper]
    number: ClassVar[IdentityField]
    index: ClassVar[IndexField]
    schema: ClassVar[ConstantField]
    type: ClassVar[RequestTypeField]
    topic: ClassVar[ReferencedEntityField]
    created_by: ClassVar[ReferencedEntityField]
    receiver: ClassVar[ReferencedEntityField]
    reviewers: ClassVar[MultiReferenceEntityField]
    status: ClassVar[RequestStatusField]
    is_closed: ClassVar[RequestStateCalculatedField]
    is_open: ClassVar[RequestStateCalculatedField]
    expires_at: ClassVar[ModelField]
    is_expired: ClassVar[ExpiredStateCalculatedField]

class RequestEventFormat(Enum):
    HTML = "html"

class RequestEvent(Record):
    model_cls: ClassVar[type[RecordMetadata]]
    schema: ClassVar[ConstantField]
    request: ClassVar[ModelField]
    request_id: ClassVar[DictField]
    type: ClassVar[EventTypeField]
    index: ClassVar[IndexField]
    check_referenced: ClassVar[Callable[..., Any]]
    created_by: ClassVar[ReferencedEntityField]
