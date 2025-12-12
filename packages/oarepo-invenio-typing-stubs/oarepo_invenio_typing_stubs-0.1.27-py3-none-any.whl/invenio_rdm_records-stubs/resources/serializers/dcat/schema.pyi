from __future__ import annotations

from typing import Any, Mapping, Optional

import idutils as idutils
from invenio_base import invenio_url_for as invenio_url_for
from invenio_rdm_records.resources.serializers.datacite.schema import (
    DataCite43Schema as DataCite43Schema,
)
from marshmallow import ValidationError as ValidationError
from marshmallow import fields as fields
from marshmallow import missing as missing
from marshmallow import validate as validate
from marshmallow_utils.html import sanitize_unicode as sanitize_unicode

class DcatSchema(DataCite43Schema):
    _files: fields.Method
    def get_files(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
    def get_subjects(
        self, obj: Mapping[str, Any]
    ) -> Optional[list[Mapping[str, Any]]]: ...
