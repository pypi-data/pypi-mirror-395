from __future__ import annotations

from typing import Any, Mapping, Optional

from flask_resources.serializers import BaseSerializerSchema as BaseSerializerSchema
from invenio_base import invenio_url_for as invenio_url_for
from invenio_rdm_records.resources.serializers.schemas import (
    CommonFieldsMixin as CommonFieldsMixin,
)
from invenio_rdm_records.resources.serializers.ui.schema import (
    current_default_locale as current_default_locale,
)
from invenio_rdm_records.resources.serializers.utils import (
    get_vocabulary_props as get_vocabulary_props,
)
from marshmallow import fields as fields
from marshmallow import missing as missing

class DublinCoreSchema(BaseSerializerSchema, CommonFieldsMixin):
    contributors: fields.Method
    titles: fields.Method
    creators: fields.Method
    identifiers: fields.Method
    relations: fields.Method
    rights: fields.Method
    dates: fields.Method
    subjects: fields.Method
    descriptions: fields.Method
    publishers: fields.Method
    types: fields.Method
    sources: fields.Constant
    languages: fields.Method
    locations: fields.Method
    formats: fields.Method

    def _transform_identifier(self, identifier: str, scheme: str) -> str: ...
    def get_identifiers(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_relations(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_rights(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_dates(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_descriptions(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_subjects(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_types(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_languages(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_formats(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
