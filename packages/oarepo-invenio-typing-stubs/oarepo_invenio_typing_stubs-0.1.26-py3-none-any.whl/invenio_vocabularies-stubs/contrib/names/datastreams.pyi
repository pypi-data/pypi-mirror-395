from collections.abc import Generator
from typing import Any, Dict, Optional, Tuple

from invenio_vocabularies.contrib.names.s3client import S3OrcidClient as S3OrcidClient
from invenio_vocabularies.datastreams import StreamEntry as StreamEntry
from invenio_vocabularies.datastreams.errors import TransformerError as TransformerError
from invenio_vocabularies.datastreams.readers import BaseReader as BaseReader
from invenio_vocabularies.datastreams.readers import (
    SimpleHTTPReader as SimpleHTTPReader,
)
from invenio_vocabularies.datastreams.transformers import (
    BaseTransformer as BaseTransformer,
)
from invenio_vocabularies.datastreams.writers import ServiceWriter as ServiceWriter
from werkzeug.utils import cached_property

class OrcidDataSyncReader(BaseReader):
    s3_client: Any
    since: Any
    def __init__(
        self, origin=None, mode: str = "r", since=None, *args, **kwargs
    ) -> None: ...
    def read(self, item=None, *args, **kwargs) -> Generator[Any, None, None]: ...

class OrcidHTTPReader(SimpleHTTPReader):
    def __init__(self, *args, test_mode: bool = True, **kwargs) -> None: ...

DEFAULT_NAMES_EXCLUDE_REGEX: str

class OrcidOrgToAffiliationMapper:
    def __init__(self, org_ids_mapping=None, org_ids_mapping_file=None) -> None: ...
    @cached_property
    def org_ids_mapping(self) -> Dict[Tuple[str, str], str]: ...
    def __call__(self, org_scheme: str, org_id: str) -> Optional[str]: ...

class OrcidTransformer(BaseTransformer):
    def __init__(
        self,
        *args,
        names_exclude_regex=...,
        org_id_to_affiliation_id_func=None,
        **kwargs,
    ) -> None: ...
    def org_id_to_affiliation_id(self, org_scheme, org_id): ...
    def apply(self, stream_entry: StreamEntry, **kwargs: Any) -> StreamEntry: ...

class NamesServiceWriter(ServiceWriter):
    def __init__(self, *args, **kwargs) -> None: ...
    def _entry_id(self, entry: Dict[str, Any]) -> Any: ...

VOCABULARIES_DATASTREAM_READERS: dict[str, type[OrcidHTTPReader | OrcidDataSyncReader]]
VOCABULARIES_DATASTREAM_TRANSFORMERS: dict[str, type[OrcidTransformer]]
VOCABULARIES_DATASTREAM_WRITERS: dict[str, type[NamesServiceWriter]]
DATASTREAM_CONFIG: Dict[str, Any]
ORCID_PRESET_DATASTREAM_CONFIG: Dict[str, Any]
