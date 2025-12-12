# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record Service components module."""

from invenio_records_resources.services.records.components.base import ServiceComponent
from invenio_records_resources.services.records.components.data import DataComponent
from invenio_records_resources.services.records.components.files import (
    BaseRecordFilesComponent,
    FilesComponent,
)
from invenio_records_resources.services.records.components.metadata import (
    MetadataComponent,
)
from invenio_records_resources.services.records.components.relations import (
    ChangeNotificationsComponent,
    RelationsComponent,
)

__all__ = (
    "ServiceComponent",
    "DataComponent",
    "MetadataComponent",
    "RelationsComponent",
    "ChangeNotificationsComponent",
    "BaseRecordFilesComponent",
    "FilesComponent",
)
