from typing import Any

from invenio_records.dumpers.base import Dumper

class SearchDumperExt:
    def dump(self, record: Any, data: dict[str, Any]) -> None: ...
    def load(self, data: dict[str, Any], record_cls: type) -> None: ...

class SearchDumper(Dumper):
    def __init__(
        self,
        extensions: list[SearchDumperExt] | None = ...,
        model_fields: dict[str, tuple[str, type]] | None = ...,
    ) -> None: ...
    @staticmethod
    def _sa_type(model_cls: type, model_field_name: str) -> type | None: ...
    @staticmethod
    def _serialize(value: Any, dump_type: type | None) -> Any: ...
    @staticmethod
    def _deserialize(value: Any, dump_type: type | None) -> Any: ...
    def _dump_model_field(
        self,
        record: Any,
        model_field_name: str,
        dump: dict[str, Any],
        dump_key: str,
        dump_type: type | None,
    ) -> None: ...
    def _load_model_field(
        self,
        record_cls: type,
        model_field_name: str,
        dump: dict[str, Any],
        dump_key: str,
        dump_type: type | None,
    ) -> Any: ...
    @staticmethod
    def _iter_modelfields(record_cls: type): ...
    def dump(self, record: Any, data: dict[str, Any]) -> dict[str, Any]: ...
    def load(self, dump_data: dict[str, Any], record_cls: type) -> Any: ...
