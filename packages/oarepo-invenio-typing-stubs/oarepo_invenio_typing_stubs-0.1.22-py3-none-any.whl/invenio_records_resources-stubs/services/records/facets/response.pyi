# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2020-2024 Northwestern University.
# Copyright (C) 2021-2024 TU Wien.
# Copyright (C) 2023-2024 Graz University of Technology.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

from __future__ import annotations

from collections.abc import Generator
from typing import Any, Self

from invenio_search.engine import dsl

class FacetsResponse(dsl.response.Response):  # type: ignore[misc]
    @classmethod
    def create_response_cls(cls, facets_param: Any) -> type[Self]: ...
    def _iter_facets(self) -> Generator[tuple[str, Any, Any, Any], None, None]: ...
    @property
    def facets(self) -> dsl.AttrDict: ...
    @property
    def labelled_facets(self) -> dsl.AttrDict: ...
