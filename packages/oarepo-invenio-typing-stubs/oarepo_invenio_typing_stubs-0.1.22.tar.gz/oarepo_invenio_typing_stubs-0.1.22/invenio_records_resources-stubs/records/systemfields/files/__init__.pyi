# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Files system field."""

from invenio_records_resources.records.systemfields.files.field import FilesField
from invenio_records_resources.records.systemfields.files.manager import FilesManager

__all__ = (
    "FilesField",
    "FilesManager",
)
