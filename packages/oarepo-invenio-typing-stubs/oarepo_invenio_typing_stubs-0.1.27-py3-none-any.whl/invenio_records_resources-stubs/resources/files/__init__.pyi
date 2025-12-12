# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

from invenio_records_resources.resources.files.config import FileResourceConfig
from invenio_records_resources.resources.files.resource import FileResource

__all__ = (
    "FileResourceConfig",
    "FileResource",
)
