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
from invenio_db.uow import UnitOfWork
from invenio_records_resources.records.api import Record
from invenio_records_resources.services.records.components.base import ServiceComponent

class RelationsComponent(ServiceComponent):
    """Relations service component."""

    def read(
        self, identity: Identity, record: Record | None = None, **kwargs: Any
    ) -> None: ...

class ChangeNotificationsComponent(ServiceComponent):
    """Back Relations service component."""

    def update(
        self,
        identity: Identity,
        data: dict[str, Any] | None = None,
        record: Record | None = None,
        uow: UnitOfWork | None = None,
        **kwargs: Any,
    ) -> None: ...
