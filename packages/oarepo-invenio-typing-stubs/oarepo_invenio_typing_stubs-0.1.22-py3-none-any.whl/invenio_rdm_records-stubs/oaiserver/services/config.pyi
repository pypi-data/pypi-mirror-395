from typing import Any, ClassVar

from invenio_records_resources.services import ServiceConfig
from invenio_records_resources.services.base import EndpointLink

from .results import OAIMetadataFormatItem, OAIMetadataFormatList
from .schema import OAIPMHMetadataFormat, OAIPMHSetSchema

class SearchOptions:
    sort_default: ClassVar[str]
    sort_direction_default: ClassVar[str]
    sort_direction_options: ClassVar[dict[str, dict[str, Any]]]
    sort_options: ClassVar[dict[str, dict[str, Any]]]
    pagination_options: ClassVar[dict[str, Any]]

class OAIPMHServerServiceConfig(ServiceConfig):
    metadata_format_result_item_cls: ClassVar[type[OAIMetadataFormatItem]]
    metadata_format_result_list_cls: ClassVar[type[OAIMetadataFormatList]]

    search: ClassVar[type[SearchOptions]]

    schema: ClassVar[type[OAIPMHSetSchema]]
    metadata_format_schema: ClassVar[type[OAIPMHMetadataFormat]]

    links_item: ClassVar[dict[str, EndpointLink]]
    links_search: ClassVar[dict[str, EndpointLink]]
