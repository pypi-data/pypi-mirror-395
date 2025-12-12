from typing import Any

from invenio_vocabularies.resources.serializer import L10NString as L10NString
from marshmallow import Schema, fields

class VocabularyL10Schema(Schema):
    id: fields.String
    title: Any
