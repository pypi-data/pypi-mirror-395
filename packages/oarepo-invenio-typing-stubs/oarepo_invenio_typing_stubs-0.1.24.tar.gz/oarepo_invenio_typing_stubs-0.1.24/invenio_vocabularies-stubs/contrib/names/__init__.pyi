from invenio_vocabularies.contrib.names.resources import NamesResource as NamesResource
from invenio_vocabularies.contrib.names.resources import (
    NamesResourceConfig as NamesResourceConfig,
)
from invenio_vocabularies.contrib.names.services import NamesService as NamesService
from invenio_vocabularies.contrib.names.services import (
    NamesServiceConfig as NamesServiceConfig,
)

__all__ = ["NamesResource", "NamesResourceConfig", "NamesService", "NamesServiceConfig"]
