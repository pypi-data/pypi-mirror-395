from __future__ import annotations

from collections.abc import Callable, KeysView
from typing import Any, TypeAlias

from flask import Flask
from jsonref import JsonRef
from werkzeug.routing import Map

from . import config as config

JSONSchemaValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | dict[str, "JSONSchemaValue"]
    | list["JSONSchemaValue"]
)
JSONSchema: TypeAlias = dict[str, JSONSchemaValue]

class InvenioJSONSchemasState:
    app: Flask
    schemas: dict[str, str]
    url_map: Map

    def __init__(self, app: Flask) -> None: ...
    def register_schemas_dir(self, directory: str) -> None: ...
    def register_schema(self, directory: str, path: str) -> None: ...
    def get_schema_dir(self, path: str) -> str: ...
    def get_schema_path(self, path: str) -> str: ...
    def get_schema(
        self,
        path: str,
        with_refs: bool = False,
        resolved: bool = False,
    ) -> dict: ...  # comment in code says dict is returned
    def list_schemas(self) -> KeysView[str]: ...
    def url_to_path(self, url: str) -> str | None: ...
    def path_to_url(self, path: str) -> str | None: ...
    @property
    def loader_cls(self) -> Callable[[], Any] | None: ...
    @property
    def resolver_cls(self) -> Callable[[JSONSchema], JSONSchema] | None: ...
    def refresolver_store(self) -> dict[str, JSONSchema | JsonRef]: ...

class InvenioJSONSchemas:
    kwargs: dict[str, Any]
    _state: InvenioJSONSchemasState

    def __init__(self, app: Flask | None = None, **kwargs: Any) -> None: ...
    def init_app(
        self,
        app: Flask,
        entry_point_group: str | None = None,
        register_blueprint: bool = True,
        register_config_blueprint: str | None = None,
    ) -> InvenioJSONSchemasState: ...
    def init_config(self, app: Flask) -> None: ...
    def __getattr__(self, name: str) -> Any: ...

class InvenioJSONSchemasUI(InvenioJSONSchemas):
    def init_app(
        self,
        app: Flask,
        entry_point_group: str | None = None,
        register_blueprint: bool = True,
        register_config_blueprint: str | None = None,
    ) -> InvenioJSONSchemasState: ...

class InvenioJSONSchemasAPI(InvenioJSONSchemas):
    def init_app(
        self,
        app: Flask,
        entry_point_group: str | None = None,
        register_blueprint: bool = True,
        register_config_blueprint: str | None = None,
    ) -> InvenioJSONSchemasState: ...
