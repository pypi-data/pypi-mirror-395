from typing import Any, ClassVar, Dict

from marshmallow import Schema
from marshmallow.fields import Field

class CustomFieldsSchema(Schema):
    field_property_name: ClassVar[str]
    fields: Dict[str, Field]
    _schema: Schema

    def __init__(self, fields_var: str, *args: Any, **kwargs: Any) -> None: ...
    def _serialize(self, obj: Any, **kwargs: Any) -> Dict[str, Any]: ...
    def _deserialize(self, data: Any, **kwargs: Any) -> Dict[str, Any]: ...

class CustomFieldsSchemaUI(CustomFieldsSchema):
    field_property_name: ClassVar[str]
