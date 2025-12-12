from typing import Any, Optional

from flask import Flask
from invenio_vocabularies import config as config
from invenio_vocabularies.contrib.affiliations import (
    AffiliationsResource as AffiliationsResource,
)
from invenio_vocabularies.contrib.affiliations import (
    AffiliationsResourceConfig as AffiliationsResourceConfig,
)
from invenio_vocabularies.contrib.affiliations import (
    AffiliationsService as AffiliationsService,
)
from invenio_vocabularies.contrib.affiliations import (
    AffiliationsServiceConfig as AffiliationsServiceConfig,
)
from invenio_vocabularies.contrib.awards import AwardsResource as AwardsResource
from invenio_vocabularies.contrib.awards import (
    AwardsResourceConfig as AwardsResourceConfig,
)
from invenio_vocabularies.contrib.awards import AwardsService as AwardsService
from invenio_vocabularies.contrib.awards import (
    AwardsServiceConfig as AwardsServiceConfig,
)
from invenio_vocabularies.contrib.funders import FundersResource as FundersResource
from invenio_vocabularies.contrib.funders import (
    FundersResourceConfig as FundersResourceConfig,
)
from invenio_vocabularies.contrib.funders import FundersService as FundersService
from invenio_vocabularies.contrib.funders import (
    FundersServiceConfig as FundersServiceConfig,
)
from invenio_vocabularies.contrib.names import NamesResource as NamesResource
from invenio_vocabularies.contrib.names import (
    NamesResourceConfig as NamesResourceConfig,
)
from invenio_vocabularies.contrib.names import NamesService as NamesService
from invenio_vocabularies.contrib.names import NamesServiceConfig as NamesServiceConfig
from invenio_vocabularies.contrib.subjects import SubjectsResource as SubjectsResource
from invenio_vocabularies.contrib.subjects import (
    SubjectsResourceConfig as SubjectsResourceConfig,
)
from invenio_vocabularies.contrib.subjects import SubjectsService as SubjectsService
from invenio_vocabularies.contrib.subjects import (
    SubjectsServiceConfig as SubjectsServiceConfig,
)
from invenio_vocabularies.resources import (
    VocabulariesAdminResource as VocabulariesAdminResource,
)
from invenio_vocabularies.resources import VocabulariesResource as VocabulariesResource
from invenio_vocabularies.resources import (
    VocabulariesResourceConfig as VocabulariesResourceConfig,
)
from invenio_vocabularies.resources import (
    VocabularyTypeResourceConfig as VocabularyTypeResourceConfig,
)
from invenio_vocabularies.services.config import (
    VocabularyTypesServiceConfig as VocabularyTypesServiceConfig,
)
from invenio_vocabularies.services.service import (
    VocabulariesService as VocabulariesService,
)
from invenio_vocabularies.services.service import (
    VocabularyTypeService as VocabularyTypeService,
)

class InvenioVocabularies:
    resource: VocabulariesResource | None
    service: VocabulariesService | None
    def __init__(self, app: Optional[Flask] = None) -> None: ...
    def init_app(self, app: Flask) -> None: ...
    def init_config(self, app: Flask) -> None: ...
    def service_configs(self, app) -> object: ...
    affiliations_service: Any
    awards_service: Any
    funders_service: Any
    names_service: Any
    subjects_service: Any
    vocabularies_service: Any
    vocabulary_types_service: Any
    def init_services(self, app: Flask) -> None: ...
    affiliations_resource: Any
    funders_resource: Any
    names_resource: Any
    awards_resource: Any
    subjects_resource: Any
    vocabulary_admin_resource: Any
    def init_resource(self, app: Flask) -> None: ...

def finalize_app(app: Flask) -> None: ...
def api_finalize_app(app: Flask) -> None: ...
def init(app: Flask) -> None: ...
