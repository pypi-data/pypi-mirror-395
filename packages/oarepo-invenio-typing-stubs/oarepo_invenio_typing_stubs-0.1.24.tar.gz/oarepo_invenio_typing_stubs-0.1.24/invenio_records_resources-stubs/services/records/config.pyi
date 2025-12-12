# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 CERN.
# Copyright (C) 2020-2025 Northwestern University.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record Service API."""

from typing import Any, Callable, Generic, Mapping, TypeVar

import marshmallow as ma
from invenio_indexer.api import RecordIndexer
from invenio_records.dumpers import Dumper
from invenio_records_permissions.policies import BasePermissionPolicy
from invenio_records_resources.records import Record
from invenio_records_resources.services import EndpointLink
from invenio_records_resources.services.base import ServiceConfig
from invenio_records_resources.services.base.links import Link
from invenio_records_resources.services.records.components.base import ServiceComponent
from invenio_records_resources.services.records.params import ParamInterpreter
from invenio_records_resources.services.records.queryparser import QueryParser
from invenio_search import RecordsSearchV2

RecordT = TypeVar("RecordT", bound=Record)
SearchOptionsT = TypeVar("SearchOptionsT", bound="SearchOptions")
SchemaT = TypeVar("SchemaT", bound=ma.Schema)
IndexerT = TypeVar("IndexerT", bound=RecordIndexer)
PermissionPolicyT = TypeVar("PermissionPolicyT", bound=BasePermissionPolicy)

class SearchOptions:
    """Search options."""

    # NOTE: configs expose immutable defaults so subclasses can override
    # without mutating shared state.
    search_cls: type[RecordsSearchV2]
    query_parser_cls: type[QueryParser]
    suggest_parser_cls: type[QueryParser] | None
    sort_default: str = "bestmatch"
    sort_default_no_query: str = "newest"
    sort_options: Mapping[str, Mapping[str, Any]]
    facets: Mapping[str, Any]
    pagination_options: Mapping[str, int]
    params_interpreters_cls: tuple[type[ParamInterpreter], ...]

class RecordServiceConfig(
    ServiceConfig[PermissionPolicyT],
    Generic[RecordT, SearchOptionsT, SchemaT, IndexerT, PermissionPolicyT],
):
    """Service factory configuration."""

    # Record specific configuration
    # NOTE: defaults are immutable here as well to prevent runtime mutation.
    record_cls: type[RecordT]
    indexer_cls: type[IndexerT]
    indexer_queue_name: str
    index_dumper: Dumper | None
    # inverse relation mapping, stores which fields relate to which record type
    relations: Mapping[str, Any]

    # Search configuration
    search: type[SearchOptionsT]

    # Service schema
    schema: type[SchemaT] | None

    # Definition of those is left up to implementations
    links_item: Mapping[str, Callable[..., Any] | Link | EndpointLink]
    links_search: Mapping[str, Callable[..., Any] | Link | EndpointLink]
    components: tuple[type[ServiceComponent]]
