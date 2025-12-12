import abc
from abc import ABC
from collections.abc import Generator
from pathlib import Path
from typing import Any, Dict, Optional, Union

from invenio_vocabularies.datastreams.errors import ReaderError as ReaderError
from invenio_vocabularies.datastreams.xml import etree_to_dict as etree_to_dict
from lxml import etree

class BaseReader(ABC, metaclass=abc.ABCMeta):
    def __init__(
        self,
        origin: Optional[Union[Path, str]] = None,
        mode: str = "r",
        *args: Any,
        **kwargs: Any,
    ) -> None: ...
    def read(self, item=None, *args, **kwargs) -> Generator[Any, None, None]: ...

class YamlReader(BaseReader): ...

class TarReader(BaseReader):
    def __init__(
        self, *args, mode: str = "r|gz", regex: Optional[str] = None, **kwargs: Any
    ) -> None: ...

class SimpleHTTPReader(BaseReader):
    content_type: Optional[str]
    def __init__(
        self,
        origin: Optional[Union[Path, str]] = None,
        id: Optional[str] = None,
        ids: Optional[list[str]] = None,
        content_type: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...
    def read(self, item=None, *args, **kwargs) -> Generator[bytes, None, None]: ...

class ZipReader(BaseReader):
    def __init__(
        self,
        *args: Any,
        options: Optional[dict[str, Any]] = None,
        regex: Optional[str] = None,
        **kwargs: Any,
    ) -> None: ...

class JsonReader(BaseReader): ...
class JsonLinesReader(BaseReader): ...
class GzipReader(BaseReader): ...

class CSVReader(BaseReader):
    csv_options: Dict[str, Any]
    as_dict: bool
    def __init__(
        self,
        *args: Any,
        csv_options: Optional[dict[str, Any]] = None,
        as_dict: bool = True,
        **kwargs: Any,
    ) -> None: ...

class XMLReader(BaseReader):
    root_element: Optional[str]
    def __init__(
        self, root_element: Optional[etree._Element] = None, *args: Any, **kwargs: Any
    ) -> None: ...

class OAIPMHReader(BaseReader):
    def __init__(
        self,
        *args: Any,
        base_url: Optional[str] = None,
        metadata_prefix: Optional[str] = None,
        set: Optional[str] = None,
        from_date=None,
        until_date=None,
        verb: Optional[str] = None,
        **kwargs: Any,
    ) -> None: ...
    def read(
        self, item=None, *args, **kwargs
    ) -> Generator[Dict[str, Any], None, None]: ...

def xml_to_dict(tree: etree._Element) -> Dict[str, Any]: ...

class RDFReader(BaseReader):
    @property
    def skos_core(self): ...
    def read(
        self, item: Any = None, *args: Any, **kwargs: Any
    ) -> Generator[Dict[str, Any], None, None]: ...

class SPARQLReader(BaseReader):
    def __init__(
        self,
        origin: Optional[Union[Path, str]],
        query: str,
        mode: str = "r",
        client_params: Optional[dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None: ...
    def read(
        self, item: Any = None, *args: Any, **kwargs: Any
    ) -> Generator[Dict[str, Any], None, None]: ...
