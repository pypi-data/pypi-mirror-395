from invenio_vocabularies.resources import VocabulariesResource as VocabulariesResource
from invenio_vocabularies.services.service import (
    VocabulariesService as VocabulariesService,
)

current_service: VocabulariesService  # intentionally not using a LocalProxy[VocabulariesService] here as mypy does not understand it
current_resource: VocabulariesResource  # intentionally not using a LocalProxy[VocabulariesResource] here as mypy does not understand it
