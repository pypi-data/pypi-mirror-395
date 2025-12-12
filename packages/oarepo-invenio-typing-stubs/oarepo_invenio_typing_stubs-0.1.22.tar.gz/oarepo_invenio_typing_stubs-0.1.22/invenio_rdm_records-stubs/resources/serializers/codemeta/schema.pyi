from __future__ import annotations

from typing import Any, Mapping

from invenio_rdm_records.resources.serializers.schemaorg.schema import SchemaorgSchema

class CodemetaSchema(SchemaorgSchema):
    identifier: Any
    context: Any
    funding: Any
    embargoDate: Any

    def get_funding(self, obj: Mapping[str, Any]) -> Any: ...
    def get_embargo_date(self, obj: Mapping[str, Any]) -> Any: ...
