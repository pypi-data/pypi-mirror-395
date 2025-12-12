from typing import Any, Callable

from flask_resources import BaseListSchema as BaseListSchema
from flask_resources import BaseObjectSchema
from marshmallow import fields

def current_default_locale() -> str: ...

L10NString: Callable[..., Any]

class VocabularyL10NItemSchema(BaseObjectSchema):
    id: fields.String
    title: Any
    description: Any
    props: fields.Dict
    icon: fields.String
    tags: fields.List
