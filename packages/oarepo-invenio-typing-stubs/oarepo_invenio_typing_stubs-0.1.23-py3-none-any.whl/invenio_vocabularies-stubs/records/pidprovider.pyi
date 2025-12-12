from typing import ClassVar, Self, Type

from invenio_pidstore.providers.base import BaseProvider

class VocabularyIdProvider(BaseProvider):
    @classmethod
    def create(
        cls,
        pid_type=None,
        pid_value=None,
        object_type=None,
        object_uuid=None,
        status=None,
        **kwargs,
    ) -> Self: ...

class CustomVocabularyPIDProvider(BaseProvider):
    pid_type: ClassVar[str | None]
    @classmethod
    def create(
        cls,
        pid_type=None,
        pid_value=None,
        object_type=None,
        object_uuid=None,
        status=None,
        **kwargs,
    ) -> Self: ...

class PIDProviderFactory:
    @staticmethod
    def create(pid_type: str, base_cls=...) -> Type[CustomVocabularyPIDProvider]: ...
