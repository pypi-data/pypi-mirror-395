from typing import Any, Dict, List, Optional

from invenio_vocabularies.datastreams.datastreams import DataStream as DataStream
from invenio_vocabularies.datastreams.errors import FactoryError as FactoryError

class OptionsConfigMixin:
    CONFIG_VAR: str
    @classmethod
    def options(cls) -> Dict[str, Any]: ...

class Factory:
    FACTORY_NAME: str
    @classmethod
    def create(cls, config: Dict[str, Any]): ...

class WriterFactory(Factory, OptionsConfigMixin):
    FACTORY_NAME: str
    CONFIG_VAR: str

class ReaderFactory(Factory, OptionsConfigMixin):
    FACTORY_NAME: str
    CONFIG_VAR: str

class TransformerFactory(Factory, OptionsConfigMixin):
    FACTORY_NAME: str
    CONFIG_VAR: str

class DataStreamFactory:
    @classmethod
    def create(
        cls,
        readers_config: List[Dict[str, Any]],
        writers_config: List[Dict[str, Any]],
        transformers_config: Optional[List[Dict[str, Any]]] = None,
        **kwargs,
    ) -> DataStream: ...
