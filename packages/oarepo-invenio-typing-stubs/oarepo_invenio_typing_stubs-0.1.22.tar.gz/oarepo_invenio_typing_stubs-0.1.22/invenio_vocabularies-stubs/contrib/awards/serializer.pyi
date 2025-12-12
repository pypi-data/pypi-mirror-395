from typing import Any

from invenio_vocabularies.contrib.awards.schema import (
    AwardOrganizationRelationSchema as AwardOrganizationRelationSchema,
)
from invenio_vocabularies.contrib.subjects.schema import (
    SubjectRelationSchema as SubjectRelationSchema,
)
from marshmallow import Schema, fields

class IdentifierSchema(Schema):
    identifier: fields.String
    scheme: fields.String

class FunderRelationSchema(Schema):
    name: fields.String
    id: fields.String

class AwardL10NItemSchema(Schema):
    id: fields.String
    title: Any
    description: Any
    number: fields.String
    acronym: fields.String
    program: fields.String
    funder: fields.Nested
    subjects: fields.List
    identifiers: fields.List
    organizations: fields.List
