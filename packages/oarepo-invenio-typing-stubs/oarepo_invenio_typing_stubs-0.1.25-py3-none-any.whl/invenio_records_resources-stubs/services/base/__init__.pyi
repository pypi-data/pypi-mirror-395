# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Base Service API."""

from invenio_records_resources.services.base.config import ServiceConfig
from invenio_records_resources.services.base.links import (
    ConditionalLink,
    EndpointLink,
    ExternalLink,
    Link,
    LinksTemplate,
    NestedLinks,
)
from invenio_records_resources.services.base.results import (
    ServiceItemResult,
    ServiceListResult,
)
from invenio_records_resources.services.base.service import Service

__all__ = (
    "ConditionalLink",
    "EndpointLink",
    "ExternalLink",
    "Link",
    "LinksTemplate",
    "Service",
    "ServiceConfig",
    "ServiceItemResult",
    "ServiceListResult",
    "NestedLinks",
)
