from __future__ import annotations

from typing import TypeAlias

from flask_resources.deserializers.base import DeserializerMixin

JSONValue: TypeAlias = (
    str | int | float | bool | None | dict[str, "JSONValue"] | list["JSONValue"]
)

class JSONDeserializer(DeserializerMixin):
    def deserialize(
        self, data: str | bytes | bytearray | memoryview | None
    ) -> JSONValue | None: ...
