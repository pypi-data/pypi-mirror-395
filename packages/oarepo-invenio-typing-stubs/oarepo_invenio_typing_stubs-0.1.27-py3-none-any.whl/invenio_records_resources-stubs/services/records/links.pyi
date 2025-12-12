# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2020-2024 Northwestern University.
# Copyright (C) 2021-2024 TU Wien.
# Copyright (C) 2023-2024 Graz University of Technology.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from __future__ import annotations

from typing import Any

from invenio_records_resources.records.api import Record
from invenio_records_resources.services.base.links import EndpointLink, Link

def pagination_endpoint_links(
    endpoint: str, params: list[str] | None = ...
) -> dict[str, EndpointLink]: ...
def pagination_links(tpl: str) -> dict[str, Link]: ...

class RecordLink(Link):
    @staticmethod
    def vars(record: Record, vars: dict[str, Any]) -> None: ...

class RecordEndpointLink(EndpointLink):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @staticmethod
    def vars(obj: Any, vars: dict[str, Any]) -> None: ...
