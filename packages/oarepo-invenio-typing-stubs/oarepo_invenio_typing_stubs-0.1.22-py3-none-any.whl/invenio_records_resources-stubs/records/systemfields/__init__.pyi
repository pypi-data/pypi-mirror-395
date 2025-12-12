# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""System fields for records."""

from invenio_records_resources.records.systemfields.files import FilesField
from invenio_records_resources.records.systemfields.index import IndexField
from invenio_records_resources.records.systemfields.pid import ModelPIDField, PIDField
from invenio_records_resources.records.systemfields.pid_statuscheck import (
    PIDStatusCheckField,
)
from invenio_records_resources.records.systemfields.relations import (
    PIDListRelation,
    PIDNestedListRelation,
    PIDRelation,
)

__all__ = (
    "FilesField",
    "IndexField",
    "ModelPIDField",
    "PIDField",
    "PIDStatusCheckField",
    "PIDRelation",
    "PIDListRelation",
    "PIDNestedListRelation",
)
