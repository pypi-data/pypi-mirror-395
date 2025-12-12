# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2025 CESNET.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Files service components."""

from invenio_records_resources.services.files.components.base import (
    FileServiceComponent,
)
from invenio_records_resources.services.files.components.content import (
    FileContentComponent,
)
from invenio_records_resources.services.files.components.metadata import (
    FileMetadataComponent,
)
from invenio_records_resources.services.files.components.multipart import (
    FileMultipartContentComponent,
)
from invenio_records_resources.services.files.components.processor import (
    FileProcessorComponent,
)

__all__ = (
    "FileContentComponent",
    "FileMetadataComponent",
    "FileProcessorComponent",
    "FileServiceComponent",
    "FileMultipartContentComponent",
)
