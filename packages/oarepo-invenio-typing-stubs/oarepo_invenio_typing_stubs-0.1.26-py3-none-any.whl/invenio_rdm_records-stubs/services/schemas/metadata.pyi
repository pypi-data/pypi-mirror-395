from __future__ import annotations

from typing import Any

from marshmallow import Schema
from marshmallow import fields as fields

record_personorg_schemes: Any
record_identifiers_schemes: Any
record_location_schemes: Any

class PersonOrOrganizationSchema(Schema):
    NAMES: list[str]
    type: fields.Str
    name: fields.Str
    given_name: fields.Str
    family_name: fields.Str
    identifiers: fields.List
    def validate_names(self, data, **kwargs): ...
    def update_names(self, data, **kwargs): ...

def validate_affiliations_data(data) -> None: ...

class CreatorSchema(Schema):
    person_or_org: fields.Nested
    role: fields.Dict
    affiliations: fields.List
    def validate_affiliations(self, data, **kwargs): ...

class ContributorSchema(Schema):
    person_or_org: fields.Nested
    role: fields.Dict
    affiliations: fields.List
    def validate_affiliations(self, data, **kwargs): ...

class TitleSchema(Schema):
    title: fields.Str
    type: fields.Str
    lang: fields.Str

class DescriptionSchema(Schema):
    description: fields.Str
    type: fields.Str
    lang: fields.Str

def _is_uri(uri) -> bool: ...

class PropsSchema(Schema):
    url: fields.Str
    scheme: fields.Str

class RightsSchema(Schema):
    id: fields.Str
    title: fields.Dict
    description: fields.Dict
    icon: fields.Str
    props: fields.Dict
    link: fields.Str
    def validate_title(self, value): ...
    def validate_description(self, value): ...
    def validate_rights(self, data, **kwargs): ...

class DateSchema(Schema):
    date: fields.Str
    type: fields.Str
    description: fields.Str

class RelatedIdentifierSchema(Schema):
    relation_type: fields.Str
    resource_type: fields.Str
    def validate_related_identifier(self, data, **kwargs): ...

class FundingSchema(Schema):
    funder: fields.Dict
    award: fields.Dict

class ReferenceSchema(Schema):
    reference: fields.Str

class PointSchema(Schema):
    lat: fields.Float
    lon: fields.Float

class LocationSchema(Schema):
    geometry: fields.Dict
    place: fields.Dict
    identifiers: fields.List
    description: fields.Str
    def validate_data(self, data, **kwargs): ...

class FeatureSchema(Schema):
    features: fields.List

class MetadataSchema(Schema):
    resource_type: fields.Dict
    creators: fields.List
    title: fields.Str
    additional_titles: fields.List
    publisher: fields.Str
    publication_date: fields.Str
    subjects: fields.List
    contributors: fields.List
    dates: fields.List
    languages: fields.List
    identifiers: fields.List
    related_identifiers: fields.List
    sizes: fields.List
    formats: fields.List
    version: fields.Str
    rights: fields.List
    copyright: fields.Str
    description: fields.Str
    additional_descriptions: fields.List
    locations: fields.Dict
    funding: fields.List
    references: fields.List
