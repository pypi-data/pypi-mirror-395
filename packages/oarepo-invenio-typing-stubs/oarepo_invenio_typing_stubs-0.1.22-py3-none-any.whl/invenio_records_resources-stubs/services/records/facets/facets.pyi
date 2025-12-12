# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2023 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Facets types defined."""

from collections.abc import Iterable
from typing import Any, Callable

from invenio_search.engine import dsl  # type: ignore[import-untyped]
from opensearch_dsl.response.aggs import FieldBucket, FieldBucketData

class LabelledFacetMixin:
    """Mixin class for overwriting the default get_values() method."""

    _label: str
    _value_labels: dict[str, str] | Callable[[list[str]], dict[str, str]] | None

    def __init__(
        self,
        label: str | None = None,
        value_labels: (
            dict[str, str] | Callable[[list[str]], dict[str, str]] | None
        ) = None,
        **kwargs: Any,
    ) -> None: ...
    def get_value(self, bucket: FieldBucket) -> str: ...
    def get_label_mapping(self, buckets: list[FieldBucket]) -> dict[str, str]: ...
    def get_values(self, data: Any, filter_values: list[Any]) -> dict[str, Any]: ...
    def get_labelled_values(
        self, data: Any, filter_values: list[Any]
    ) -> dict[str, Any]: ...

class TermsFacet(LabelledFacetMixin, dsl.TermsFacet):
    """Terms facet."""

    def get_values(self, data: Any, filter_values: list[Any]) -> dict[str, Any]: ...  # type: ignore[override]

class NestedTermsFacet(TermsFacet):
    """A hierarchical terms facet."""

    _field: str | None
    _subfield: str | None
    _splitchar: str

    def __init__(
        self,
        field: str | None = None,
        subfield: str | None = None,
        splitchar: str = "::",
        **kwargs: Any,
    ) -> None: ...
    def get_aggregation(self) -> Any: ...
    def _parse_values(self, filter_values: list[str]) -> dict[str, list[str]]: ...
    def get_value_filter(self, parsed_value: tuple[str, list[str]]) -> Any: ...  # type: ignore[override]
    def add_filter(self, filter_values: list[str]) -> Any: ...
    def get_values(
        self, data: Any, filter_values: list[Any], key_prefix: str | None = None
    ) -> dict[str, Any]: ...
    def get_labelled_values(
        self,
        data: FieldBucketData,
        filter_values: list[Any],
        bucket_label: bool = True,
        key_prefix: str | None = None,
    ) -> dict[str, Any]: ...

class CombinedTermsFacet(NestedTermsFacet):
    """Facet to mimic a nested aggregation without having to define a 'nested' field."""

    _field: str  # type: ignore[assignment]
    _combined_field: str
    _parents: Iterable[str] | Callable[[], Iterable[str]]
    _cached_parents: Iterable[str] | None
    _splitchar: str

    def __init__(
        self,
        field: str,
        combined_field: str,
        parents: Iterable[str] | Callable[[], Iterable[str]],
        splitchar: str = "::",
        **kwargs: Any,
    ) -> None: ...
    def get_parents(self) -> Iterable[str]: ...
    def get_aggregation(self) -> Any: ...
    def get_labelled_values(
        self,
        data: FieldBucketData,
        filter_values: list[Any],
        bucket_label: bool = True,
        key_prefix: str | None = None,
    ) -> dict[str, Any]: ...
    def get_value_filter(self, parsed_value: tuple[str, list[str]]) -> Any: ...

class CFFacetMixin:
    """Mixin to abstract the custom fields path."""

    @classmethod
    def field(cls, field: str) -> str: ...

class CFTermsFacet(CFFacetMixin, TermsFacet):
    """Terms facet for custom fields."""

    def __init__(
        self,
        field: str | None = None,
        label: str | None = None,
        value_labels: (
            dict[str, str] | Callable[[list[str]], dict[str, str]] | None
        ) = None,
        **kwargs: Any,
    ) -> None: ...

class CFNestedTermsFacet(CFFacetMixin, NestedTermsFacet):
    """Nested Terms facet for custom fields."""

    def __init__(
        self,
        field: str | None = None,
        label: str | None = None,
        value_labels: (
            dict[str, str] | Callable[[list[str]], dict[str, str]] | None
        ) = None,
        **kwargs: Any,
    ) -> None: ...
