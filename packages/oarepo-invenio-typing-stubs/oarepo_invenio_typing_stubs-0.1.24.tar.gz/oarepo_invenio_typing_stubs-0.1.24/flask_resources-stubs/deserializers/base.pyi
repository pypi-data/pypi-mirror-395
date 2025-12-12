from __future__ import annotations

from typing import Any

class DeserializerMixin:
    def deserialize(self, data: Any) -> Any: ...

class LoaderMixin:
    @staticmethod
    def post_load(data: Any, **kwargs: Any) -> Any: ...
    @staticmethod
    def pre_load(data: Any, **kwargs: Any) -> Any: ...
