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

class RecordRelationLabels:
    relation: Any  # Relation field
    lookup_key: str
    def __init__(self, relation: Any, lookup_key: str) -> None: ...
    def __call__(self, ids: list[str]) -> dict[str, Any]: ...
