from typing import (
    Any,
    Dict,
    Optional,
    Self,
    Tuple,
    Type,
    Union,
    overload,
)

from invenio_records.api import Record
from invenio_records.dumpers.search import SearchDumper
from invenio_records.extensions import ExtensionMixin, RecordExtension, RecordMeta

def _get_fields(
    attrs: Any, field_class: Type[SystemField]
) -> Dict[str, SystemField]: ...
def _get_inherited_fields(
    class_: Type[SystemFieldsMixin], field_class: Type[SystemField]
) -> Dict[Any, Any]: ...

#
# How to type SystemField
#
# SystemField is a Descriptor, so it needs to be typed as such. A descriptor returns
# a different value for __get__(instance=None, owner=clz) (usually itself but can be
# something else) and for __get__(instance=instance, owner=clz) (usually some kind of
# context or a manager, but for example, for ConstantField actually the value itself).
#
# To capture this, a Descriptor and a GenericDescriptor is defined in oarepo_typing/descriptors.py \
# that allows to specify the different return types.
#
# SystemField is also a generic class, with two type parameters:
#  - R - the type of the Record it is attached to (usually a subclass of Record)
#  - V - the type of the value it holds
#
# Usage:
#  class PIDField(SystemField[Record, PIDFieldContext]): ...
#
# TODO: we do not have a good way of handling special SystemField that return something
# else than themselves when accessed on class. For these, add a GenericDescriptor mixin
# to override this behaviour.
#

class SystemField(ExtensionMixin):
    def __init__(self, key: Optional[str] = ...): ...
    @property
    def attr_name(self) -> str: ...
    @property
    def key(self) -> str: ...
    def get_dictkey(self, instance: Record) -> Any: ...
    def set_dictkey(
        self, instance: Record, value: Any, create_if_missing: bool = False
    ) -> None: ...
    def _set_cache(self, instance: Record, obj: Any) -> None: ...
    def _get_cache(self, instance: Record) -> Any: ...
    @overload
    def __get__(self, instance: None, owner: type[Record]) -> Self: ...
    @overload
    def __get__(self, instance: Record, owner: type[Record]) -> Any: ...
    @overload
    def __set__(self, instance: None, value: Self) -> None: ...
    @overload
    def __set__(self, instance: Record, value: Any) -> None: ...

class SystemFieldsMixin(metaclass=SystemFieldsMeta):
    """Mixin for classes that support system fields."""

    pass

class SystemFieldContext:
    @property
    def field(self) -> SystemField: ...

class SystemFieldsExt(RecordExtension):
    def __init__(self, declared_fields: Dict[str, SystemField]): ...
    def _run(self, method: str, *args, **kwargs): ...
    def post_commit(self, *args, **kwargs): ...
    def post_create(self, *args, **kwargs): ...
    def post_delete(self, *args, **kwargs): ...
    def post_revert(self, *args, **kwargs): ...
    def pre_commit(self, *args, **kwargs): ...
    def pre_create(self, *args, **kwargs): ...
    def pre_delete(self, *args, **kwargs): ...
    def pre_init(self, *args, **kwargs): ...
    def pre_load(
        self,
        data: Dict[str, Optional[Union[str, int]]],
        loader: Optional[SearchDumper] = ...,
    ): ...
    def pre_revert(self, *args, **kwargs): ...

class SystemFieldsMeta(RecordMeta):
    @staticmethod
    def __new__(
        mcs: Type[SystemFieldsMeta],
        name: str,
        bases: Tuple[()],
        attrs: Dict[str, Union[str, int, Tuple[()]]],
    ) -> SystemFieldsMeta: ...
