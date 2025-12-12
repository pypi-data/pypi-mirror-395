from typing import Any, Mapping, Optional

from flask_resources import BaseObjectSchema
from invenio_vocabularies.resources import VocabularyL10Schema
from marshmallow import Schema, fields

from .fields import AccessStatusField

def current_default_locale() -> str: ...
def make_affiliation_index(attr: str, obj: Mapping[str, Any], *args: Any) -> Mapping[str, Any] | fields._MissingType: ...  # type: ignore[name-defined]
def record_version(obj: Mapping[str, Any]) -> str: ...
def get_coordinates(obj: Mapping[str, Any]) -> Optional[Any]: ...

class RelatedIdentifiersSchema(Schema):
    identifier: fields.String
    relation_type: fields.Nested
    scheme: fields.String
    resource_type: fields.Nested

class AdditionalTitlesSchema(Schema):
    title: fields.String
    type: fields.Nested
    lang: fields.Nested

class AdditionalDescriptionsSchema(Schema):
    description: fields.Field
    type: fields.Nested
    lang: fields.Nested

class DatesSchema(Schema):
    date: fields.String
    type: fields.Nested
    description: fields.Field

class RightsSchema(VocabularyL10Schema):
    description: fields.Field
    icon: fields.Str
    link: fields.String
    props: fields.Dict

class FundingSchema(Schema):
    award: fields.Nested
    funder: fields.Nested

class GeometrySchema(Schema):
    type: fields.Str
    coordinates: fields.Function

class IdentifierSchema(Schema):
    scheme: fields.Str
    identifier: fields.Str

class FeatureSchema(Schema):
    place: fields.Field
    description: fields.Field
    geometry: fields.Nested
    identifiers: fields.List

class LocationSchema(Schema):
    features: fields.List

class MeetingSchema(Schema):
    acronym: fields.Field
    dates: fields.Field
    place: fields.Field
    session_part: fields.Field
    session: fields.Field
    title: fields.Field
    url: fields.Field

def compute_publishing_information(obj: Mapping[str, Any]) -> Mapping[str, str] | fields._MissingType: ...  # type: ignore[name-defined]

class TombstoneSchema(Schema):
    removal_reason: fields.Nested
    note: fields.String
    removed_by: fields.Function
    removal_date_l10n_medium: fields.Field
    removal_date_l10n_long: fields.Field
    citation_text: fields.String
    is_visible: fields.Boolean

class UIRecordSchema(BaseObjectSchema):
    publication_date_l10n_medium: fields.Field
    publication_date_l10n_long: fields.Field
    created_date_l10n_long: fields.Field
    updated_date_l10n_long: fields.Field
    resource_type: fields.Nested
    additional_titles: fields.List
    custom_fields: fields.Nested
    publishing_information: fields.Function
    conference: fields.Nested
    access_status: AccessStatusField
    creators: fields.Function
    contributors: fields.Function
    languages: fields.List
    description_stripped: fields.Field
    version: fields.Function
    related_identifiers: fields.List
    additional_descriptions: fields.List
    dates: fields.List
    rights: fields.List
    is_draft: fields.Boolean
    funding: fields.List
    tombstone: fields.Nested
    locations: fields.Nested

    def add_communities_permissions_and_roles(
        self, obj: Mapping[str, Any], **kwargs: Any
    ) -> Mapping[str, Any]: ...
    def hide_tombstone(
        self, obj: Mapping[str, Any], **kwargs: Any
    ) -> Mapping[str, Any]: ...
