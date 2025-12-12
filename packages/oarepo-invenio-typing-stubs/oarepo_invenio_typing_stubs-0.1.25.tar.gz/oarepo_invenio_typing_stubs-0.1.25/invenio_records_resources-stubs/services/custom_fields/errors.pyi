from abc import abstractmethod
from typing import Set

class CustomFieldsException(Exception):
    @property
    @abstractmethod
    def description(self) -> str: ...

class CustomFieldsInvalidArgument(CustomFieldsException):
    arg_name: str
    def __init__(self, arg_name: str): ...
    @property
    def description(self) -> str: ...

class CustomFieldsNotConfigured(CustomFieldsException):
    field_names: Set[str]
    def __init__(self, field_names: Set[str]): ...
    @property
    def description(self) -> str: ...

class InvalidCustomFieldsNamespace(CustomFieldsException):
    field_name: str
    given_namespace: str
    def __init__(self, field_name: str, given_namespace: str): ...
    @property
    def description(self) -> str: ...
