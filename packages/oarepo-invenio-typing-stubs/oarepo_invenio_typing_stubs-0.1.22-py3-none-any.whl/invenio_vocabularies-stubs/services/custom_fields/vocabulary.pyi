from typing import Any, ClassVar

import marshmallow as ma
from flask_principal import Identity
from invenio_records_resources.records.systemfields import PIDListRelation, PIDRelation
from invenio_records_resources.services.custom_fields.base import BaseCF
from invenio_vocabularies.proxies import current_service as current_service
from invenio_vocabularies.records.api import Vocabulary as Vocabulary
from invenio_vocabularies.records.systemfields.pid import (
    VocabularyPIDFieldContext as VocabularyPIDFieldContext,
)
from invenio_vocabularies.resources.serializer import (
    VocabularyL10NItemSchema as VocabularyL10NItemSchema,
)
from invenio_vocabularies.services.schema import (
    VocabularyRelationSchema as VocabularyRelationSchema,
)
from marshmallow.fields import Field

class VocabularyCF(BaseCF):
    field_keys: ClassVar[list[str]]
    relation_cls: type[PIDRelation] | type[PIDListRelation]
    vocabulary_id: str
    dump_options: bool
    multiple: bool
    sort_by: str | None
    schema: type[ma.Schema]
    ui_schema: type[ma.Schema]
    pid_field: VocabularyPIDFieldContext
    def __init__(
        self,
        name: str,
        vocabulary_id: str,
        multiple: bool = False,
        dump_options: bool = True,
        sort_by: str | None = None,
        schema: type[ma.Schema] = ...,
        ui_schema: type[ma.Schema] = ...,
        **kwargs: Any,
    ) -> None: ...
    def options(self, identity: Identity) -> list[dict[str, Any]] | None: ...
    @property
    def field(self) -> Field: ...
    @property
    def ui_field(self) -> Field: ...
    @property
    def mapping(self) -> dict[str, Any]: ...
