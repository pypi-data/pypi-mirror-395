from __future__ import annotations

from collections.abc import Callable
from typing import Any

from flask_resources.serializers.base import BaseSerializer

class SimpleSerializer(BaseSerializer):
    _encoder: Callable[[Any], str]

    def __init__(self, encoder: Callable[[Any], str]) -> None: ...
    def serialize_object(self, obj: Any, **kwargs: Any) -> str: ...
    def serialize_object_list(self, obj_list: Any, **kwargs: Any) -> str: ...

__all__ = ("SimpleSerializer",)
