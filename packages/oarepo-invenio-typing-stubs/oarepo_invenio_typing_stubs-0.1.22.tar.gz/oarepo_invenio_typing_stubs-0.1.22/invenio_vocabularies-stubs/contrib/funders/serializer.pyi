from typing import Any

from invenio_vocabularies.resources import L10NString as L10NString
from marshmallow import Schema, fields

class IdentifierSchema(Schema):
    identifier: fields.String
    scheme: fields.String

class FunderL10NItemSchema(Schema):
    id: fields.String
    title: Any
    description: Any
    props: fields.Dict
    name: fields.String
    country: fields.String
    country_name: fields.String
    identifiers: fields.List
