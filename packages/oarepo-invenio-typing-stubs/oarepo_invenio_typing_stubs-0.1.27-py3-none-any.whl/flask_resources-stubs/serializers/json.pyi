from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any, Protocol

from flask_resources.serializers.base import BaseSerializer

def flask_request_options() -> dict[str, Any]: ...

class JSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any: ...

class _EncoderFactory(Protocol):
    def __call__(self) -> json.JSONEncoder: ...

OptionsResolvable = dict[str, Any] | Callable[[], dict[str, Any]]
EncoderResolvable = type[json.JSONEncoder] | _EncoderFactory

class JSONSerializer(BaseSerializer):
    _options: OptionsResolvable | None
    _encoder: EncoderResolvable | json.JSONEncoder

    def __init__(
        self,
        encoder: EncoderResolvable | json.JSONEncoder | None = ...,
        options: OptionsResolvable | None = ...,
    ) -> None: ...
    @property
    def dumps_options(self) -> dict[str, Any]: ...
    @property
    def encoder(self) -> type[json.JSONEncoder]: ...
    def serialize_object(self, obj: Any) -> str: ...
    def serialize_object_list(self, obj_list: Any) -> str: ...

__all__ = ("JSONSerializer", "JSONEncoder", "flask_request_options")
