from __future__ import annotations

from typing import Any, Mapping, Optional

from dateutil.parser import parse as parse
from dojson.contrib.to_marc21.fields.bdleader import to_leader as to_leader
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
from marshmallow_utils.html import sanitize_unicode as sanitize_unicode
from pydash import py_ as py_

class MARCXMLSchema(BaseSerializerSchema, CommonFieldsMixin):
    id: fields.Method
    doi: fields.Method
    oai: fields.Method
    contributors: fields.Method
    titles: fields.Method
    first_creator: fields.Method
    relations: fields.Method
    rights: fields.Method
    license: fields.Method
    subjects: fields.Method
    descriptions: fields.Method
    additional_descriptions: fields.Method
    languages: fields.Method
    references: fields.Method
    publication_information: fields.Method
    dissertation_note: fields.Method
    types_and_community_ids: fields.Method
    formats: fields.Method
    sizes: fields.Method
    funding: fields.Method
    updated: fields.Method
    files: fields.Method
    access: fields.Method
    host_information: fields.Method
    leader: fields.Method

    def get_leader(self, obj: Mapping[str, Any]) -> Any: ...
    def get_host_information(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_access(self, obj: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def get_files(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_sizes(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_communities(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_formats(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_doi(self, obj: Mapping[str, Any]) -> Mapping[str, Any] | None: ...
    def get_oai(self, obj: Mapping[str, Any]) -> Mapping[str, Any] | None: ...
    def _serialize_contributor(
        self, contributor: Mapping[str, Any]
    ) -> Mapping[str, Any]: ...
    def get_contributors(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_first_creator(self, obj: Mapping[str, Any]) -> Mapping[str, Any] | None: ...
    def get_pub_information(
        self, obj: Mapping[str, Any]
    ) -> Mapping[str, Any] | None: ...
    def get_dissertation_note(
        self, obj: Mapping[str, Any]
    ) -> Mapping[str, Any] | None: ...
    def get_titles(self, obj: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def get_updated(self, obj: Mapping[str, Any]) -> str: ...
    def get_id(self, obj: Mapping[str, Any]) -> str: ...
    def get_funding(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_relations(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_rights(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_license(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def _serialize_description(self, description: str) -> Mapping[str, Any]: ...
    def get_descriptions(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_additional_descriptions(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_languages(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_references(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_subjects(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_types_and_communities(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
