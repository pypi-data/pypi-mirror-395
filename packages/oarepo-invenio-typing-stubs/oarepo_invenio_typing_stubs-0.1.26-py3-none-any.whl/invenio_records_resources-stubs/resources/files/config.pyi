# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020-2025 Northwestern University.
# Copyright (C) 2025 CESNET.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""File resource configuration."""

from typing import Callable, Mapping

from flask import Response
from flask_resources import ResourceConfig
from werkzeug.exceptions import HTTPException

class FileResourceConfig(ResourceConfig):
    """File resource config."""

    # NOTE: annotate with immutable-friendly types so overriding subclasses
    # replace defaults instead of mutating shared class state.
    blueprint_name: str | None = None
    url_prefix: str | None = "/records/<pid_value>"
    routes: Mapping[str, str]
    error_handlers: Mapping[
        int | type[HTTPException] | type[BaseException],
        Callable[[Exception], Response],
    ]
