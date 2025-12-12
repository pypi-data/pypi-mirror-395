from typing import Any, Iterable

from flask import Flask

class _SearchState:
    app: Flask
    mappings: dict[str, str]
    aliases: dict[str, dict[str, str]]
    current_suffix: str
    cluster_version: list[int]
    cluster_distribution: str
    active_aliases: dict[str, dict[str, str]]
    entry_point_group_templates: str | None
    entry_point_group_component_templates: str | None
    entry_point_group_index_templates: str | None
    _client: Any | None
    _current_suffix: str | None

    def __init__(
        self,
        app: Flask,
        entry_point_group_mappings: str | None = ...,
        entry_point_group_templates: str | None = ...,
        entry_point_group_component_templates: str | None = ...,
        entry_point_group_index_templates: str | None = ...,
        **kwargs: Any,
    ) -> None: ...
    @property
    def templates(self) -> dict[str, str]: ...
    @property
    def component_templates(self) -> dict[str, str]: ...
    @property
    def index_templates(self) -> dict[str, str]: ...
    @property
    def client(self) -> Any: ...
    @staticmethod
    def _get_mappings_module(module: str) -> str: ...
    def _collect_templates(self, entrypoint_group: str) -> dict[str, str]: ...
    def _client_builder(self) -> Any: ...
    def _get_indices(self, tree_or_filename: dict[str, Any]) -> Iterable[str]: ...
    def _replace_prefix(
        self, template_path: str, body: str, enforce_prefix: bool
    ) -> str: ...
    def _put_template(
        self,
        template_name: str,
        template_file: str,
        put_function: Any,
        ignore: list[int] | None,
        enforce_prefix: bool = ...,
    ) -> tuple[str, Any]: ...
    def register_mappings(self, alias: str, package_name: str) -> None: ...
    def register_templates(self, module: str) -> dict[str, str]: ...
    def load_entry_point_group_mappings(
        self, entry_point_group_mappings: str
    ) -> None: ...
    def create(
        self,
        ignore: list[int] | None = ...,
        ignore_existing: bool = ...,
        index_list: list[str] | None = ...,
    ) -> Iterable[tuple[str, Any]]: ...
    def create_index(
        self,
        index: str,
        mapping_path: str | None = ...,
        prefix: str | None = ...,
        suffix: str | None = ...,
        create_write_alias: bool = ...,
        ignore: list[int] | None = ...,
        dry_run: bool = ...,
    ) -> tuple[tuple[str, Any | None], tuple[str | None, Any | None]]: ...
    def update_mapping(self, index: str, check: bool = ...) -> None: ...
    def put_templates(
        self, ignore: list[int] | None = ...
    ) -> Iterable[tuple[str, Any]]: ...
    def put_component_templates(
        self, ignore: list[int] | None = ...
    ) -> Iterable[tuple[str, Any]]: ...
    def put_index_templates(
        self, ignore: list[int] | None = ...
    ) -> Iterable[tuple[str, Any]]: ...
    def delete(
        self, ignore: list[int] | None = ..., index_list: list[str] | None = ...
    ) -> Iterable[tuple[str, Any]]: ...
    def flush_and_refresh(self, index: str) -> bool: ...

class InvenioSearch:
    _state: _SearchState
    _clients: dict[str, Any]

    def __init__(self, app: Flask | None = None, **kwargs: Any) -> None: ...
    def init_app(
        self,
        app: Flask,
        entry_point_group_mappings: str = ...,
        entry_point_group_templates: str = ...,
        entry_point_group_component_templates: str = ...,
        entry_point_group_index_templates: str = ...,
        **kwargs: Any,
    ) -> None: ...
    @staticmethod
    def init_config(app: Flask) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
