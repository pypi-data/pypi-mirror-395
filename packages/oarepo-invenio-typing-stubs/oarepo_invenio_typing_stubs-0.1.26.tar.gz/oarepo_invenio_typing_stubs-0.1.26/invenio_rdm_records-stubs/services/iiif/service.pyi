from __future__ import annotations

from typing import Any, Generic, TypeVar

from flask_principal import Identity
from invenio_records_resources.services import Service
from invenio_records_resources.services.base import ServiceConfig

C = TypeVar("C", bound=ServiceConfig)

class IIIFService(Service[C], Generic[C]):
    def __init__(self, config: Any, records_service: Any) -> None: ...
    def _iiif_uuid(self, uuid: str) -> tuple[str, str]: ...
    def _iiif_image_uuid(self, uuid: str) -> tuple[str, str, str]: ...
    def file_service(self, type_: str) -> Any: ...
    def read_record(self, identity: Identity, uuid: str) -> Any: ...
    def _open_image(self, file_: Any) -> Any: ...
    def get_file(self, identity: Identity, uuid: str, key: str | None = ...) -> Any: ...
    def image_api(
        self,
        identity: Identity,
        uuid: str,
        region: str,
        size: str,
        rotation: str,
        quality: str,
        image_format: str,
    ) -> Any: ...
