# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

from invenio_records_resources.resources.files import (
    FileResource as FileResource,
)
from invenio_records_resources.resources.files import (
    FileResourceConfig as FileResourceConfig,
)
from invenio_records_resources.resources.records import (
    RecordResource as RecordResource,
)
from invenio_records_resources.resources.records import (
    RecordResourceConfig as RecordResourceConfig,
)
from invenio_records_resources.resources.records import (
    SearchRequestArgsSchema as SearchRequestArgsSchema,
)

__all__ = (
    "FileResourceConfig",
    "FileResource",
    "RecordResource",
    "RecordResourceConfig",
    "SearchRequestArgsSchema",
)
