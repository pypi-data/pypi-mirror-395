from typing import Any

from flask_resources.serializers import DumperMixin

class JournalDataciteDumper(DumperMixin):
    def post_dump(
        self, data: dict[str, Any], original: dict[str, Any] | None = None, **kwargs
    ) -> dict[str, Any]: ...

class JournalDublinCoreDumper(DumperMixin):
    def post_dump(
        self, data: dict[str, Any], original: dict[str, Any] | None = None, **kwargs
    ) -> dict[str, Any]: ...

class JournalMarcXMLDumper(DumperMixin):
    def post_dump(
        self, data: dict[str, Any], original: dict[str, Any] | None = None, **kwargs
    ) -> dict[str, Any]: ...

class JournalCSLDumper(DumperMixin):
    def post_dump(
        self, data: dict[str, Any], original: dict[str, Any] | None = None, **kwargs
    ) -> dict[str, Any]: ...

class JournalSchemaorgDumper(DumperMixin):
    def post_dump(
        self, data: dict[str, Any], original: dict[str, Any] | None = None, **kwargs
    ) -> dict[str, Any]: ...
