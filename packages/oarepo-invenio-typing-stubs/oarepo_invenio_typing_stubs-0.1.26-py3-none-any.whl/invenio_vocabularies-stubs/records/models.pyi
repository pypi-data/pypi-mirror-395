from typing import TYPE_CHECKING, ClassVar, Optional

# Note: db.Model is used as a base class in the source. We intentionally
# avoid importing a specific db type here and instead declare a loose name
# so type checkers don't error on the base class while preserving the API shape.
from invenio_records.models import RecordMetadata
from sqlalchemy import Column

if TYPE_CHECKING:
    from invenio_records.systemfields.relatedmodelfield import RelatedModelField
    from invenio_vocabularies.records.api import Vocabulary

# Note: db.Model base comes from invenio_db.shared.SQLAlchemy.Model

class _Model:
    """Placeholder SQLAlchemy model base for stubs."""

    ...

class VocabularyType(_Model):
    __tablename__: ClassVar[str]
    id: Column
    pid_type: Column
    @classmethod
    def create(cls, **data) -> VocabularyType: ...
    @classmethod
    def dump_obj(
        cls, field: RelatedModelField, record: Vocabulary, obj: VocabularyType
    ) -> None: ...
    @classmethod
    def load_obj(
        cls, field: RelatedModelField, record: Vocabulary
    ) -> Optional[VocabularyType]: ...

class VocabularyMetadata(RecordMetadata):
    ...

class VocabularyScheme(_Model):
    __tablename__: ClassVar[str]
    id: Column
    parent_id: Column
    name: Column
    uri: Column
    @classmethod
    def create(cls, **data) -> VocabularyScheme: ...
