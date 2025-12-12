# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2023 TU Wien.
# Copyright (C) 2025 Graz University of Technology.
# Copyright (C) 2025 CESNET.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Record File Resources."""

from typing import Any, Callable, Generic, ParamSpec, TypeAlias, TypeVar

from flask.wrappers import Response
from flask_resources import Resource
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.files.config import FileResourceConfig
from invenio_records_resources.services.files.service import FileService

P = ParamSpec("P")
R = TypeVar("R")
Decorator: TypeAlias = Callable[[Callable[P, R]], Callable[P, R]]

def set_max_content_length(func: Callable[P, R]) -> Callable[P, R]: ...

# note: unlike in sources, we are having generics here so that we can safely pass and access
# instances of subclasses in inheriting resources
C = TypeVar("C", bound=FileResourceConfig)
S = TypeVar("S", bound=FileService)

class FileResource(ErrorHandlersMixin, Resource[C], Generic[C, S]):
    """File resource."""

    service: S

    def __init__(self, config: C, service: S) -> None: ...
    def create_url_rules(self) -> list[dict[str, Any]]: ...
    def search(self) -> tuple[dict[str, Any], int]: ...
    def delete_all(self) -> tuple[str, int]: ...
    def create(self) -> tuple[dict[str, Any], int]: ...
    def read(self) -> tuple[dict[str, Any], int]: ...
    def update(self) -> tuple[dict[str, Any], int]: ...
    def delete(self) -> tuple[str, int]: ...
    def create_commit(self) -> tuple[dict[str, Any], int]: ...
    def read_content(self) -> Response: ...
    def update_content(self) -> tuple[dict[str, Any], int]: ...
    def upload_multipart_content(self) -> tuple[dict[str, Any], int]: ...
    def read_archive(self) -> Response: ...

# Decorators
request_view_args: Decorator
request_data: Decorator
request_stream: Decorator
request_multipart_args: Decorator
