from typing import Callable

# note: the actual implementation uses dynamic imports, here we just import
# the opensearch libraries directly for typing purposes
import opensearch_dsl as dsl
import opensearchpy as search
from opensearchpy import OpenSearch as SearchEngine

ES: str
OS: str

SEARCH_DISTRIBUTION: str

def check_search_version(
    distribution: str, version: int | Callable[[int], bool]
) -> bool: ...
def check_es_version(version: int | Callable[[int], bool]) -> bool: ...
def check_os_version(version: int | Callable[[int], bool]) -> bool: ...
def uses_es7() -> bool: ...

# Expose the dynamically selected libraries

__all__ = (
    "ES",
    "OS",
    "SEARCH_DISTRIBUTION",
    "SearchEngine",
    "check_es_version",
    "check_os_version",
    "check_search_version",
    "dsl",
    "search",
    "uses_es7",
)
