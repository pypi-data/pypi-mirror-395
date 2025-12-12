# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Data access layer."""

from invenio_records_resources.records.api import File, FileRecord, Record
from invenio_records_resources.records.models import FileRecordModelMixin

__all__ = (
    "File",
    "FileRecord",
    "FileRecordModelMixin",
    "Record",
)
