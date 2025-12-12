from __future__ import annotations

from typing import Any

from flask import Blueprint, Flask
from flask_principal import Identity

# Keep imports minimal to avoid unresolved stub dependencies in type checkers.
from invenio_records_resources.resources.files import FileResource

def on_identity_loaded(sender: Any, identity: Identity) -> None: ...

blueprint: Blueprint

class InvenioRDMRecords:
    def __init__(self, app: Flask | None = None) -> None: ...
    def init_app(self, app: Flask) -> None: ...
    def init_config(self, app: Flask) -> None: ...
    def service_configs(self, app: Flask) -> type: ...
    def init_services(self, app: Flask) -> None: ...
    def init_resource(self, app: Flask) -> None: ...
    def fix_datacite_configs(self, app: Flask) -> None: ...

    # Services
    records_service: Any
    records_media_files_service: Any
    iiif_service: Any
    record_communities_service: Any
    community_records_service: Any
    community_inclusion_service: Any
    record_requests_service: Any
    oaipmh_server_service: Any

    # Resources
    records_resource: Any
    record_files_resource: FileResource
    draft_files_resource: FileResource
    record_media_files_resource: FileResource
    draft_media_files_resource: FileResource
    parent_record_links_resource: Any
    parent_grants_resource: Any
    grant_user_access_resource: Any
    grant_group_access_resource: Any
    record_communities_resource: Any
    record_requests_resource: Any
    community_records_resource: Any
    oaipmh_server_resource: Any
    iiif_resource: Any

def finalize_app(app: Flask) -> None: ...
def api_finalize_app(app: Flask) -> None: ...
def init(app: Flask) -> None: ...
