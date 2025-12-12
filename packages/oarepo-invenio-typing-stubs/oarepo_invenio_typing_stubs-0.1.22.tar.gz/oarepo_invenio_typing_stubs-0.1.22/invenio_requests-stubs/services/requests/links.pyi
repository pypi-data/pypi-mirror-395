from typing import Any, Dict, Optional

from flask_principal import Identity
from invenio_records_resources.pagination import Pagination
from invenio_records_resources.records.api import FileRecord, Record
from invenio_records_resources.services.base.links import Link, LinksTemplate
from invenio_requests.records.api import Request

class RequestLinksTemplate(LinksTemplate):
    def __init__(
        self,
        links: Dict[str, "RequestLink"],
        action_link: "RequestLink",
        context: Optional[Dict[str, Any]] = None,
    ) -> None: ...
    def expand(
        self, identity: Identity, obj: Record | FileRecord | Pagination | Any
    ) -> Dict[str, str]: ...

class RequestLink(Link):
    @staticmethod
    def vars(record: Request, vars: Dict[str, Any]) -> None: ...
