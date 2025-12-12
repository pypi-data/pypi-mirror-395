# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Files Service API."""

from invenio_records_resources.services.files.components import FileServiceComponent
from invenio_records_resources.services.files.config import FileServiceConfig
from invenio_records_resources.services.files.links import FileLink
from invenio_records_resources.services.files.service import FileService

__all__ = (
    "FileLink",
    "FileService",
    "FileServiceComponent",
    "FileServiceConfig",
)
