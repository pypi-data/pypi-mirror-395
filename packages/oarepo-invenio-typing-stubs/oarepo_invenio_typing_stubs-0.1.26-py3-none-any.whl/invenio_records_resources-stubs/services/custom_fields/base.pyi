from abc import ABC, ABCMeta, abstractmethod
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Type,
)

from marshmallow.fields import Field

def ensure_no_field_cls(func: Callable[..., Any]) -> Callable[..., Any]: ...

class BaseCF(ABC):
    name: str
    _field_args: Dict[str, Any]

    def __init__(
        self, name: str, field_args: Optional[Dict[str, Any]] = ...
    ) -> None: ...
    @property
    @abstractmethod
    def mapping(self) -> Any: ...
    @property
    @abstractmethod
    def field(self) -> Field: ...
    @property
    def ui_field(self) -> Field: ...
    def dump(self, record: Any, cf_key: str = ...) -> None: ...
    def load(self, record: Any, cf_key: str = ...) -> None: ...

class BaseListCF(BaseCF, metaclass=ABCMeta):
    _multiple: bool
    _field_cls: Type[Field]

    def __init__(
        self, name: str, field_cls: Type[Field], multiple: bool = ..., **kwargs: Any
    ) -> None: ...
    @property
    def field(self) -> Field: ...
