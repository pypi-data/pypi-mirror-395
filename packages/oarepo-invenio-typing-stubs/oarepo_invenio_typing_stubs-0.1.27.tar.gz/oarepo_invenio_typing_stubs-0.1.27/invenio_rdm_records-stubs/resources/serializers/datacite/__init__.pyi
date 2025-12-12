from __future__ import annotations

from typing import Any

from flask_resources import BaseListSchema as BaseListSchema
from flask_resources import MarshmallowSerializer as MarshmallowSerializer
from flask_resources.serializers import JSONSerializer as JSONSerializer
from flask_resources.serializers import SimpleSerializer as SimpleSerializer
from invenio_rdm_records.contrib.journal.processors import (
    JournalDataciteDumper as JournalDataciteDumper,
)
from invenio_rdm_records.resources.serializers.datacite.schema import (
    DataCite43Schema as DataCite43Schema,
)

class DataCite43JSONSerializer(MarshmallowSerializer):
    def __init__(self, **options: Any) -> None: ...

class DataCite43XMLSerializer(MarshmallowSerializer):
    def __init__(self, **options: Any) -> None: ...
