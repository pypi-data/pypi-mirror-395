from __future__ import annotations

from jsonref import JsonRef

from .ext import InvenioJSONSchemasState, JSONSchema

current_jsonschemas: InvenioJSONSchemasState  # intentionally not using a LocalProxy[InvenioJSONSchemasState] here as mypy does not understand it
current_refresolver_store: dict[
    str, JSONSchema | JsonRef
]  # intentionally not using a LocalProxy[dict[str, JSONSchema | JsonRef]] here as mypy does not understand it
