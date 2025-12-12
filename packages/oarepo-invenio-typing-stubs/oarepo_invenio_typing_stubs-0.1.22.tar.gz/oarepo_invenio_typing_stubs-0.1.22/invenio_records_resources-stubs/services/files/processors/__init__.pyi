"""Files processing API."""

from invenio_records_resources.services.files.processors.base import (
    FileProcessor,
    ProcessorRunner,
)
from invenio_records_resources.services.files.processors.image import (
    ImageMetadataExtractor,
)

__all__ = (
    "FileProcessor",
    "ImageMetadataExtractor",
    "ProcessorRunner",
)
