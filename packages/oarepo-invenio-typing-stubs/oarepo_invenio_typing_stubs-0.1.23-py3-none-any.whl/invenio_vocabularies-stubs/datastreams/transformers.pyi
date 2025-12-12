import abc
from abc import ABC, abstractmethod
from typing import Any, Optional

from invenio_vocabularies.datastreams import StreamEntry as StreamEntry
from invenio_vocabularies.datastreams.errors import TransformerError as TransformerError
from invenio_vocabularies.datastreams.xml import etree_to_dict as etree_to_dict
from lxml import etree

class BaseTransformer(ABC, metaclass=abc.ABCMeta):
    @abstractmethod
    def apply(
        self, stream_entry: StreamEntry, *args: Any, **kwargs: Any
    ) -> StreamEntry: ...

class XMLTransformer(BaseTransformer):
    root_element: Optional[str]
    def __init__(self, root_element=None, *args, **kwargs) -> None: ...
    @classmethod
    def _xml_to_etree(cls, xml: str) -> etree._Element | None: ...
    def apply(self, stream_entry: StreamEntry, **kwargs: Any) -> StreamEntry: ...

class RDFTransformer(BaseTransformer):
    @property
    def skos_core(self): ...
    def apply(
        self, stream_entry: StreamEntry, *args: Any, **kwargs: Any
    ) -> StreamEntry: ...
