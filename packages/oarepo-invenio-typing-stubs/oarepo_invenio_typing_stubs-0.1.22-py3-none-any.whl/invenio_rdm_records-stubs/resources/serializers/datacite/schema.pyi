from __future__ import annotations

from typing import Any, Mapping, Optional

from babel_edtf import parse_edtf as parse_edtf
from edtf.parser.grammar import ParseException as ParseException
from flask import current_app as current_app
from flask_resources.serializers import BaseSerializerSchema as BaseSerializerSchema
from invenio_access.permissions import system_identity as system_identity
from invenio_base import invenio_url_for as invenio_url_for
from invenio_rdm_records.proxies import (
    current_rdm_records_service as current_rdm_records_service,
)
from invenio_rdm_records.resources.serializers.ui.schema import (
    current_default_locale as current_default_locale,
)
from invenio_rdm_records.resources.serializers.utils import (
    get_preferred_identifier as get_preferred_identifier,
)
from invenio_rdm_records.resources.serializers.utils import (
    get_vocabulary_props as get_vocabulary_props,
)
from marshmallow import Schema as Schema
from marshmallow import ValidationError as ValidationError
from marshmallow import fields as fields
from marshmallow import missing as missing
from marshmallow import post_dump as post_dump
from marshmallow import validate as validate
from marshmallow_utils.fields import SanitizedUnicode as SanitizedUnicode
from marshmallow_utils.html import strip_html as strip_html
from pydash import py_ as py_

RELATED_IDENTIFIER_SCHEMES: set[str]

def get_scheme_datacite(
    scheme: str, config_name: str, default: str | None = None
) -> str | None: ...

class PersonOrOrgSchema43(Schema):
    name: fields.Str
    nameType: fields.Method
    givenName: fields.Str
    familyName: fields.Str
    nameIdentifiers: fields.Method
    affiliation: fields.Method
    def get_name_type(self, obj: Mapping[str, Any]) -> str: ...
    def get_name_identifiers(
        self, obj: Mapping[str, Any]
    ) -> list[Mapping[str, Any]]: ...
    def get_affiliation(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    @post_dump(pass_many=False)
    def capitalize_name_type(
        self, data: Mapping[str, Any], **kwargs: Any
    ) -> Mapping[str, Any]: ...

class CreatorSchema43(PersonOrOrgSchema43): ...

class ContributorSchema43(PersonOrOrgSchema43):
    contributorType: fields.Method
    def get_role(self, obj: Mapping[str, Any]) -> Optional[str]: ...

class SubjectSchema43(Schema):
    subject: fields.Str
    valueURI: fields.Str
    subjectScheme: fields.Str

class DataCite43Schema(BaseSerializerSchema):
    types: fields.Method
    titles: fields.Method
    creators: fields.List
    contributors: fields.List
    publisher: fields.Str
    publicationYear: fields.Method
    subjects: fields.Method
    dates: fields.Method
    language: fields.Method
    identifiers: fields.Method
    relatedIdentifiers: fields.Method
    sizes: fields.List
    formats: fields.List
    version: SanitizedUnicode
    rightsList: fields.Method
    descriptions: fields.Method
    geoLocations: fields.Method
    fundingReferences: fields.Method
    schemaVersion: fields.Constant
    def get_type(self, obj: Mapping[str, Any]) -> Optional[Mapping[str, str]]: ...
    def _merge_main_and_additional(
        self, obj: Mapping[str, Any], field: str, default_type: Optional[str] = None
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_titles(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_descriptions(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_publication_year(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_dates(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_language(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_identifiers(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_related_identifiers(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_locations(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_subjects(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_rights(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_funding(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
