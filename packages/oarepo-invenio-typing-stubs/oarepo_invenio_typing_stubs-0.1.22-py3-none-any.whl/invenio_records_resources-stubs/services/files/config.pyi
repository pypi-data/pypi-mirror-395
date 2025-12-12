from typing import Any, Mapping

from invenio_records_resources.services.base import ServiceConfig
from invenio_records_resources.services.files.processors import (
    FileProcessor,
)
from invenio_records_resources.services.files.results import FileItem, FileList
from invenio_records_resources.services.files.schema import FileSchema

class FileServiceConfig(ServiceConfig):
    # NOTE: use immutable defaults so subclasses can override without
    # mutating shared state across instances.
    record_cls: type[Any] | None
    permission_action_prefix: str

    file_result_item_cls: type[FileItem]
    file_result_list_cls: type[FileList]
    file_schema: type[FileSchema]

    max_files_count: int

    file_links_list: Mapping[str, Any]
    file_links_item: Mapping[str, Any]

    allow_upload: bool
    allow_archive_download: bool

    file_processors: tuple[FileProcessor, ...]
