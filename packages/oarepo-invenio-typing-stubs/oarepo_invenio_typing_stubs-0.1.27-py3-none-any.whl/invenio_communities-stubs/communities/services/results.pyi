from collections.abc import Generator
from typing import Any, Dict, List, Optional, Union

from flask_principal import Identity
from flask_sqlalchemy.pagination import QueryPagination
from invenio_communities.communities.services.links import CommunityLinksTemplate
from invenio_communities.communities.services.service import CommunityService
from invenio_records_resources.services.base.links import LinksTemplate
from invenio_records_resources.services.records.results import RecordItem, RecordList
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper
from invenio_requests.services.results import EntityResolverExpandableField

class CommunityListResult(RecordList):
    def __init__(
        self,
        service: CommunityService,
        identity: Identity,
        results: QueryPagination,
        params: Optional[Dict[str, Union[str, int]]] = None,
        links_tpl: Optional[LinksTemplate] = None,
        links_item_tpl: Optional[CommunityLinksTemplate] = None,
        schema: Optional[ServiceSchemaWrapper] = None,
        expandable_fields: Optional[List[EntityResolverExpandableField]] = None,
        expand: bool = False,
    ) -> None: ...
    @property
    def hits(self) -> Generator[Dict[str, Any], None, None]: ...

class CommunityFeaturedList(CommunityListResult):
    def __len__(self) -> int: ...
    def __iter__(self): ...
    @property
    def total(self) -> int: ...
    @property
    def hits(self) -> Generator[Dict[str, Any], None, None]: ...

class CommunityItem(RecordItem):
    @property
    def links(self) -> Dict[str, str]: ...
    def to_dict(self) -> Dict[str, Any]: ...

class FeaturedCommunityItem(CommunityItem): ...
