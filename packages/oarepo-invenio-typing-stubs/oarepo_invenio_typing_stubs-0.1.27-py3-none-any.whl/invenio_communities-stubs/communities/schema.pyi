from typing import Any, Dict

from invenio_records_resources.services.records.schema import BaseRecordSchema
from invenio_vocabularies.contrib.affiliations.schema import (
    AffiliationRelationSchema as BaseAffiliationRelationSchema,
)
from invenio_vocabularies.services.schema import (
    VocabularyRelationSchema as VocabularySchema,
)
from marshmallow import EXCLUDE, Schema, fields, post_dump, post_load, pre_load
from marshmallow.validate import Length
from marshmallow_utils.permissions import FieldPermissionsMixin

def _not_blank(**kwargs: Any) -> Length: ...
def no_longer_than(max: int, **kwargs: Any) -> Length: ...
def is_not_uuid(value: str) -> None: ...

class CommunityAccessSchema(Schema):
    visibility: fields.Str
    members_visibility: fields.Str
    member_policy: fields.Str
    record_policy: fields.Str
    record_submission_policy: fields.Str
    review_policy: fields.Str

class AffiliationRelationSchema(BaseAffiliationRelationSchema):
    class Meta:
        unknown = EXCLUDE

class CommunityMetadataSchema(Schema):
    title: fields.Str
    description: fields.Str
    curation_policy: fields.Str
    page: fields.Str
    type: fields.Nested
    website: fields.Url
    funding: fields.List
    organizations: fields.List

class AgentSchema(Schema):
    user: fields.Str

class RemovalReasonSchema(VocabularySchema):
    id: fields.Str

class TombstoneSchema(Schema):
    removal_reason: fields.Nested
    note: fields.Str
    removed_by: fields.Nested
    removal_date: fields.Str
    citation_text: fields.Str
    is_visible: fields.Bool

class DeletionStatusSchema(Schema):
    is_deleted: fields.Bool
    status: fields.Str

class CommunityThemeStyleSchema(Schema):
    font: fields.Dict
    primaryColor: fields.Str
    secondaryColor: fields.Str
    tertiaryColor: fields.Str
    primaryTextColor: fields.Str
    secondaryTextColor: fields.Str
    tertiaryTextColor: fields.Str
    mainHeaderBackgroundColor: fields.Str

class CommunityThemeSchema(Schema):
    style: fields.Nested
    brand: fields.Str
    enabled: fields.Bool

class ChildrenSchema(Schema):
    allow: fields.Bool

class BaseCommunitySchema(BaseRecordSchema, FieldPermissionsMixin):
    class Meta:
        unknown = EXCLUDE

    field_dump_permissions: Dict[str, str]
    id: fields.Str
    slug: fields.Str
    metadata: fields.Nested
    access: fields.Nested
    custom_fields: fields.Nested
    is_verified: fields.Bool
    theme: fields.Nested
    tombstone: fields.Nested
    deletion_status: fields.Nested
    children: fields.Nested
    @post_dump
    def post_dump(
        self, data: Dict[str, Any], many: bool, **kwargs: Any
    ) -> Dict[str, Any]: ...

class CommunityParentSchema(BaseCommunitySchema): ...

class CommunitySchema(BaseCommunitySchema):
    parent: fields.Nested
    @post_dump
    def post_dump(
        self, data: Dict[str, Any], many: bool, **kwargs: Any
    ) -> Dict[str, Any]: ...
    def filter_parent_id(
        self, in_data: Dict[str, Any], original_data: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]: ...
    @pre_load
    def initialize_custom_fields(
        self, data: Dict[str, Any], **kwargs: Any
    ) -> Dict[str, Any]: ...
    @post_load
    def lowercase(self, in_data: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]: ...

class CommunityFeaturedSchema(Schema):
    id: fields.Int
    start_date: fields.DateTime

class CommunityGhostSchema(Schema):
    id: fields.Str
    metadata: fields.Constant
