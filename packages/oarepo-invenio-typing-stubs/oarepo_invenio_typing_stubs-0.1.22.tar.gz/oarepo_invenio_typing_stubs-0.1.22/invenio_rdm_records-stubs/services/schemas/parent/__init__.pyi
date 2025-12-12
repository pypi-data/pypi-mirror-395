from typing import Any

from invenio_drafts_resources.services.records.schema import ParentSchema
from marshmallow import fields
from marshmallow_utils.fields import NestedAttribute
from marshmallow_utils.permissions import FieldPermissionsMixin

def validate_scheme(scheme: str) -> None: ...

class RDMParentSchema(ParentSchema, FieldPermissionsMixin):
    field_dump_permissions: dict[str, str]
    access: fields.Nested
    review: fields.Nested
    communities: NestedAttribute
    pids: fields.Dict
    is_verified: fields.Boolean
    def clean(self, data: dict[str, Any], **kwargs: Any) -> dict[str, Any]: ...
    def clean_review(self, data: dict[str, Any], **kwargs: Any) -> dict[str, Any]: ...
    def pop_review_if_none(
        self, data: dict[str, Any], many: bool, **kwargs: Any
    ) -> dict[str, Any]: ...

__all__ = ("RDMParentSchema",)
