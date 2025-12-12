# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record Service API."""

from invenio_records_resources.services.records.config import (
    RecordServiceConfig,
    SearchOptions,
)
from invenio_records_resources.services.records.links import (
    RecordEndpointLink,
    RecordLink,
    pagination_endpoint_links,
    pagination_links,
)
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from invenio_records_resources.services.records.service import (
    RecordIndexerMixin,
    RecordService,
)

__all__ = (
    "pagination_endpoint_links",
    "pagination_links",
    "RecordEndpointLink",
    "RecordLink",
    "RecordService",
    "RecordServiceConfig",
    "SearchOptions",
    "ServiceSchemaWrapper",
    "RecordIndexerMixin",
)
