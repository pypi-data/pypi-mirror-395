from typing import Any

from invenio_search.ext import _SearchState

def _get_current_search() -> _SearchState: ...
def _get_current_search_client() -> Any: ...

current_search: _SearchState  # intentionally not using a LocalProxy[_SearchState] here as mypy does not understand it
current_search_client: (
    Any  # intentionally not using a LocalProxy[Any] here as mypy does not understand it
)
