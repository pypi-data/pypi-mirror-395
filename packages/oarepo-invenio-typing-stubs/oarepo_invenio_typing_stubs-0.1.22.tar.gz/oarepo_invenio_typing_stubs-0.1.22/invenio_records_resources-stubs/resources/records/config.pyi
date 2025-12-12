# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record Resource Configuration."""

from typing import Any, Mapping

import marshmallow as ma
from flask_resources import RequestBodyParser, ResourceConfig, ResponseHandler
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema

class RecordResourceConfig(ResourceConfig):
    """Record resource config."""

    # Blueprint configuration
    # NOTE: use immutable-friendly annotations to avoid shared mutable state.
    blueprint_name: str | None = None
    url_prefix: str | None = "/records"
    routes: Mapping[str, str]

    # Request parsing
    request_read_args: Mapping[str, Any]
    request_view_args: Mapping[str, ma.fields.Field]
    request_search_args: type[SearchRequestArgsSchema]
    request_extra_args: Mapping[str, ma.fields.Field]
    request_headers: Mapping[str, ma.fields.Field]
    request_body_parsers: Mapping[str, RequestBodyParser]
    default_content_type: str | None

    # Response handling
    response_handlers: Mapping[str, ResponseHandler]
    default_accept_mimetype: str | None
