# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Files request body parser."""

from typing import IO

class RequestStreamParser:
    """Parse the request body."""

    def parse(self) -> dict[str, int | IO[bytes] | None]: ...
