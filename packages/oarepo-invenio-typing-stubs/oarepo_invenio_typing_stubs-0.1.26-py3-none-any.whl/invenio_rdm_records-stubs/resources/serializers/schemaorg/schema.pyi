from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional

import pycountry as pycountry
from babel_edtf import parse_edtf as parse_edtf
from commonmeta import dict_to_spdx as dict_to_spdx
from commonmeta import doi_as_url as doi_as_url
from commonmeta import parse_attributes as parse_attributes
from commonmeta import unwrap as unwrap
from commonmeta import wrap as wrap
from edtf.parser.grammar import ParseException as ParseException
from flask_resources.serializers import BaseSerializerSchema as BaseSerializerSchema
from idutils import to_url as to_url
from invenio_rdm_records.resources.serializers.schemas import (
    CommonFieldsMixin as CommonFieldsMixin,
)
from invenio_rdm_records.resources.serializers.utils import (
    convert_size as convert_size,
)
from invenio_rdm_records.resources.serializers.utils import (
    get_vocabulary_props as get_vocabulary_props,
)
from marshmallow import Schema as Schema
from marshmallow import ValidationError as ValidationError
from marshmallow import fields as fields
from marshmallow import missing as missing
from marshmallow_utils.fields import SanitizedHTML as SanitizedHTML
from marshmallow_utils.fields import SanitizedUnicode as SanitizedUnicode
from pydash import py_ as py_

def _serialize_identifiers(
    ids: Iterable[Mapping[str, Any]],
) -> list[Mapping[str, Any]]: ...

class PersonOrOrgSchema(Schema):
    name: fields.Str
    givenName: fields.Str
    familyName: fields.Str
    affiliation: fields.Method
    id_: fields.Method
    type_: fields.Method
    def _serialize_identifier(self, identifier: Mapping[str, Any]) -> Optional[str]: ...
    def get_name_type(self, obj: Mapping[str, Any]) -> str: ...
    def get_name_identifier(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_affiliation(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...

class SchemaorgSchema(BaseSerializerSchema, CommonFieldsMixin):
    context: Any
    id_: fields.Method
    type_: fields.Method
    identifier: fields.Method
    name: SanitizedUnicode
    creator: fields.List
    author: fields.List
    editor: fields.List
    publisher: fields.Method
    keywords: fields.Method
    dateCreated: fields.Method
    dateModified: fields.Method
    datePublished: fields.Method
    temporal: fields.Method
    inLanguage: fields.Method
    contentSize: fields.Method
    size: fields.Method
    encodingFormat: fields.Method
    version: SanitizedUnicode
    license: fields.Method
    description: SanitizedHTML
    funding: fields.Method
    isPartOf: fields.Method
    hasPart: fields.Method
    sameAs: fields.Method
    citation: fields.Method
    url: fields.Method
    measurementTechnique: fields.Method
    distribution: fields.Method
    uploadDate: fields.Method

    def get_id(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_type(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_size(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_format(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_publication_date(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_creation_date(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_modification_date(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_language(self, obj: Mapping[str, Any]) -> Optional[Mapping[str, Any]]: ...
    def get_identifiers(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_spatial_coverage(self, obj: Mapping[str, Any]) -> Any: ...
    def get_publisher(self, obj: Mapping[str, Any]) -> Optional[Mapping[str, Any]]: ...
    def get_keywords(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_license(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_funding(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_is_part_of(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_has_part(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_sameAs(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_url(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_dates(self, obj: Mapping[str, Any]) -> Optional[list[str]]: ...
    def get_citation(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def _is_dataset(self, obj: Mapping[str, Any]) -> bool: ...
    def get_measurement_techniques(self, obj: Mapping[str, Any]) -> Optional[str]: ...
    def get_distribution(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def _filter_related_identifier_type(
        self,
        identifiers: Iterable[Mapping[str, Any]],
        relation_types: Iterable[str] | str,
    ): ...
    def _is_video(self, obj: Mapping[str, Any]) -> bool: ...
    def get_upload_date(self, obj: Mapping[str, Any]) -> Optional[str]: ...
