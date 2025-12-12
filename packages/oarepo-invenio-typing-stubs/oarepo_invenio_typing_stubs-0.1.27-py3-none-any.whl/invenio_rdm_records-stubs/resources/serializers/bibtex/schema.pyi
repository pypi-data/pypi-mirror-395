from __future__ import annotations

from typing import Any

from flask_resources.serializers import BaseSerializerSchema
from invenio_rdm_records.resources.serializers.bibtex.schema_formats import (
    BibTexFormatter as BibTexFormatter,
)
from invenio_rdm_records.resources.serializers.schemas import CommonFieldsMixin

class BibTexSchema(BaseSerializerSchema, CommonFieldsMixin):
    id: Any
    resource_id: Any
    version: Any
    date_published: Any
    locations: Any
    titles: Any
    doi: Any
    creators: Any
    creator: Any
    publishers: Any
    contributors: Any
    school: Any
    journal: Any
    volume: Any
    booktitle: Any
    number: Any
    pages: Any
    note: Any
    venue: Any
    url: Any

    entry_mapper: dict[str, list[dict[str, Any]]]

    @property
    def default_entry_type(
        self,
    ) -> dict[str, Any]: ...  # keep typing: uses BibTexFormatter.misc shape
    def get_id(self, obj: dict[str, Any]) -> str: ...
    def get_date_published(self, obj: dict[str, Any]) -> dict[str, str] | None: ...
    def get_creator(self, obj: dict[str, Any]) -> dict[str, str]: ...
    def get_booktitle(self, obj: dict[str, Any]) -> str | None: ...
    def get_pages(self, obj: dict[str, Any]) -> str | None: ...
    def get_venue(self, obj: dict[str, Any]) -> str | None: ...
    def get_note(self, obj: dict[str, Any]) -> str | None: ...
    def get_number(self, obj: dict[str, Any]) -> str | None: ...
    def get_volume(self, obj: dict[str, Any]) -> str | None: ...
    def get_journal(self, obj: dict[str, Any]) -> str | None: ...
    def get_school(self, obj: dict[str, Any]) -> str | None: ...
    def get_url(self, obj: dict[str, Any]) -> str | None: ...
    def dump_record(
        self, data: dict[str, Any], original: dict[str, Any], many: bool, **kwargs: Any
    ) -> str: ...
    def _get_bibtex_entry(
        self, resource_type: str, fields_map: dict[str, Any]
    ) -> dict[str, Any]: ...
    def _dump_data(
        self,
        name: str,
        entry_fields: list[str],
        fields: dict[str, Any],
        data: dict[str, Any],
        original: dict[str, Any],
    ) -> str: ...
    def _parse_fields(self, entry_fields: list[str], fields: dict[str, Any]) -> str: ...
    def _fetch_fields_map(self, data: dict[str, Any]) -> dict[str, Any]: ...
    def _format_output_row(self, field: str, value: Any) -> str: ...
    def _get_citation_key(
        self, data: dict[str, Any], original_data: dict[str, Any]
    ) -> str: ...
    def _clean_input(self, input: str) -> str: ...
