from typing import TYPE_CHECKING, Any

from invenio_records.systemfields import ModelField

if TYPE_CHECKING:
    from invenio_requests.records.api import Request

class IdentityField(ModelField):
    def assign(self, record: "Request", **kwargs: Any) -> str: ...
