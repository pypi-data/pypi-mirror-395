from typing import Any

from flask_resources.serializers import DumperMixin

class MeetingDublinCoreDumper(DumperMixin):
    def post_dump(
        self, data: dict[str, Any], original: dict[str, Any] | None = None, **kwargs
    ) -> dict[str, Any]: ...

class MeetingCSLDumper(DumperMixin):
    def post_dump(
        self, data: dict[str, Any], original: dict[str, Any] | None = None, **kwargs
    ) -> dict[str, Any]: ...
