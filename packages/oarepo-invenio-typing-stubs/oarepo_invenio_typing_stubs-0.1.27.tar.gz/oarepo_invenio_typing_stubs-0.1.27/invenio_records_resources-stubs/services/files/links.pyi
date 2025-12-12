from typing import Any, Dict

from invenio_records_resources.services.base import EndpointLink, Link

class FileLink(Link):
    @staticmethod
    def vars(obj: Any, vars: Dict[str, Any]) -> None: ...

class FileEndpointLink(EndpointLink):
    @staticmethod
    def vars(obj: Any, vars: Dict[str, Any]) -> None: ...
