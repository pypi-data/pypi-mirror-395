from __future__ import annotations

from .ext import (
    InvenioJSONSchemas as InvenioJSONSchemas,
)
from .ext import (
    InvenioJSONSchemasAPI as InvenioJSONSchemasAPI,
)
from .ext import (
    InvenioJSONSchemasUI as InvenioJSONSchemasUI,
)
from .proxies import current_jsonschemas as current_jsonschemas

__version__: str

__all__ = (
    "__version__",
    "InvenioJSONSchemas",
    "InvenioJSONSchemasUI",
    "InvenioJSONSchemasAPI",
    "current_jsonschemas",
)
