import re
from typing import Any, Dict, List, Optional, Type

from invenio_vocabularies.datastreams.readers import CSVReader as CSVReader
from invenio_vocabularies.datastreams.readers import GzipReader as GzipReader
from invenio_vocabularies.datastreams.readers import JsonLinesReader as JsonLinesReader
from invenio_vocabularies.datastreams.readers import JsonReader as JsonReader
from invenio_vocabularies.datastreams.readers import OAIPMHReader as OAIPMHReader
from invenio_vocabularies.datastreams.readers import RDFReader as RDFReader
from invenio_vocabularies.datastreams.readers import (
    SimpleHTTPReader as SimpleHTTPReader,
)
from invenio_vocabularies.datastreams.readers import SPARQLReader as SPARQLReader
from invenio_vocabularies.datastreams.readers import TarReader as TarReader
from invenio_vocabularies.datastreams.readers import XMLReader as XMLReader
from invenio_vocabularies.datastreams.readers import YamlReader as YamlReader
from invenio_vocabularies.datastreams.readers import ZipReader as ZipReader
from invenio_vocabularies.datastreams.transformers import (
    XMLTransformer as XMLTransformer,
)
from invenio_vocabularies.datastreams.writers import AsyncWriter as AsyncWriter
from invenio_vocabularies.datastreams.writers import ServiceWriter as ServiceWriter
from invenio_vocabularies.datastreams.writers import YamlWriter as YamlWriter
from invenio_vocabularies.resources import (
    VocabulariesResourceConfig as VocabulariesResourceConfig,
)
from invenio_vocabularies.services.config import (
    VocabulariesServiceConfig as VocabulariesServiceConfig,
)

VOCABULARIES_RESOURCE_CONFIG = VocabulariesResourceConfig
VOCABULARIES_SERVICE_CONFIG = VocabulariesServiceConfig
VOCABULARIES_IDENTIFIER_SCHEMES: Dict[str, Dict[str, Any]]
edmo_regexp: re.Pattern[str]

def is_pic(val: str) -> bool: ...
def is_edmo(val: str) -> re.Match[str] | None: ...

VOCABULARIES_AFFILIATION_SCHEMES: Dict[str, Dict[str, Any]]
VOCABULARIES_FUNDER_SCHEMES: Dict[str, Dict[str, Any]]
VOCABULARIES_FUNDER_DOI_PREFIX: str
VOCABULARIES_AWARD_SCHEMES: Dict[str, Dict[str, Any]]
VOCABULARIES_AWARDS_OPENAIRE_FUNDERS: Dict[str, str]
VOCABULARIES_AWARDS_EC_ROR_ID: str
VOCABULARIES_NAMES_SCHEMES: Dict[str, Dict[str, Any]]
VOCABULARIES_SUBJECTS_SCHEMES: Dict[str, Dict[str, Any]]
VOCABULARIES_CUSTOM_VOCABULARY_TYPES: List[str]
VOCABULARIES_DATASTREAM_READERS: Dict[str, Type[Any]]
VOCABULARIES_DATASTREAM_TRANSFORMERS: Dict[str, Type[Any]]
VOCABULARIES_DATASTREAM_WRITERS: Dict[str, Type[Any]]
VOCABULARIES_TYPES_SORT_OPTIONS: Dict[str, Dict[str, Any]]
VOCABULARIES_TYPES_SEARCH: Dict[str, Any]
VOCABULARIES_SUBJECTS_EUROSCIVOC_FILE_URL: str
VOCABULARIES_SUBJECTS_GEMET_FILE_URL: str
VOCABULARIES_SUBJECTS_NVS_FILE_URL: str
VOCABULARIES_AFFILIATIONS_EDMO_COUNTRY_MAPPING: Dict[str, str]
VOCABULARIES_ORCID_ACCESS_KEY: str
VOCABULARIES_ORCID_SECRET_KEY: str
VOCABULARIES_ORCID_SUMMARIES_BUCKET: str
VOCABULARIES_ORCID_SYNC_MAX_WORKERS: int
VOCABULARIES_ORCID_SYNC_SINCE: Dict[str, int]
VOCABULARIES_ORCID_ORG_IDS_MAPPING_PATH: Optional[str]
