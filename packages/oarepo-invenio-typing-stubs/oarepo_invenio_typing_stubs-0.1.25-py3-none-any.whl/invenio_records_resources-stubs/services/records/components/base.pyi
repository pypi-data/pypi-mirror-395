# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2022 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records service component base classes."""

from typing import Any

from flask_principal import Identity
from invenio_records_resources.services.base.components import BaseServiceComponent
from invenio_search.api import RecordsSearchV2

class ServiceComponent(BaseServiceComponent):
    """Base service component."""

    def create(self, identity: Identity, **kwargs: Any) -> None: ...
    def read(self, identity: Identity, **kwargs: Any) -> None: ...
    def update(self, identity: Identity, **kwargs: Any) -> None: ...
    def delete(self, identity: Identity, **kwargs: Any) -> None: ...
    def search(
        self,
        identity: Identity,
        search: RecordsSearchV2,
        params: dict[str, Any],
        **kwargs: Any,
    ) -> RecordsSearchV2: ...
