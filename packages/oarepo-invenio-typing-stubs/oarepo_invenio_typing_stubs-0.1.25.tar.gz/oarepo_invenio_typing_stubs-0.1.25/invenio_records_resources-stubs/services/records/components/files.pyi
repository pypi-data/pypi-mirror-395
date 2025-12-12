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
from invenio_records_resources.records.api import Record
from invenio_records_resources.services.base.service import Service
from invenio_records_resources.services.records.components.base import ServiceComponent

class FileConfigMixin:
    """Mixin class adding dynamic file loading."""

    _files_attr_key: str | None = None
    _files_data_key: str | None = None
    _files_bucket_attr_key: str | None = None
    _files_bucket_id_attr_key: str | None = None

    @property
    def files_attr_key(self) -> str | None: ...
    @property
    def files_data_key(self) -> str | None: ...
    @property
    def files_bucket_attr_key(self) -> str | None: ...
    @property
    def files_bucket_id_attr_key(self) -> str | None: ...
    def get_record_files(self, record: Record) -> Any: ...  # FilesManager
    def get_record_bucket(self, record: Record) -> Any: ...  # Bucket
    def get_record_bucket_id(self, record: Record) -> str: ...

class BaseRecordFilesComponent(FileConfigMixin, ServiceComponent):
    def __init__(self, service: Service) -> None: ...
    def _validate_files_enabled(self, record: Record, enabled: bool) -> None: ...
    def assign_files_enabled(self, record: Record, enabled: bool) -> None: ...
    def assign_files_default_preview(
        self, record: Record, default_preview: str | None
    ) -> None: ...
    def create(
        self,
        identity: Identity,
        data: dict[str, Any] | None = None,
        record: Record | None = None,
        errors: list[Any] | None = None,
        **kwargs: Any,
    ) -> None: ...
    def update(
        self,
        identity: Identity,
        data: dict[str, Any] | None = None,
        record: Record | None = None,
        **kwargs: Any,
    ) -> None: ...

FilesAttrConfig: dict[str, str]

FilesComponent: type[BaseRecordFilesComponent]
