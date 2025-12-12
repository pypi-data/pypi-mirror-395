from typing import Any

from marshmallow.schema import Schema

class SubjectSchema(Schema): ...

def validate_rat(token) -> tuple[int, dict[str, Any]]: ...
