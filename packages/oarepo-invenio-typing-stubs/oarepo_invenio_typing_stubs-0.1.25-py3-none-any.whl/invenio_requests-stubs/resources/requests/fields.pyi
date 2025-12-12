from typing import Any, Dict, Mapping, Optional

from marshmallow import fields

class ReferenceString(fields.Field):
    default_error_messages: Dict[str, str]

    def _deserialize(
        self,
        value: Optional[str],
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs: Any,
    ) -> Optional[Dict[str, str]]: ...
    def _serialize(
        self, value: Any, attr: Optional[str], obj: Any, **kwargs: Any
    ) -> str: ...
