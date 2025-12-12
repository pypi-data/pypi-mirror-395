# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

from typing import Any, Mapping

def etag_headers(
    obj_or_list: Mapping[str, Any], code: int, many: bool = False
) -> dict[str, str]: ...
