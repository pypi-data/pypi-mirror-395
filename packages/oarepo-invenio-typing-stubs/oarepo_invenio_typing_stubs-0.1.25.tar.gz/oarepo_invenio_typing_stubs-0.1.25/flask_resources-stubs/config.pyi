from __future__ import annotations

from typing import Any, Protocol, TypeVar

class SupportsConfigAttribute(Protocol):
    def __getattr__(self, name: str) -> Any: ...

T = TypeVar("T")

class ConfigAttrValue[T]:
    config_attr: str

    def __init__(self, config_attr: str) -> None: ...
    def resolve(self, config: SupportsConfigAttribute) -> T: ...

U = TypeVar("U")

def resolve_from_conf(
    val: ConfigAttrValue[U] | U, config: SupportsConfigAttribute
) -> U: ...
def from_conf(config_attr: str) -> ConfigAttrValue[Any]: ...
