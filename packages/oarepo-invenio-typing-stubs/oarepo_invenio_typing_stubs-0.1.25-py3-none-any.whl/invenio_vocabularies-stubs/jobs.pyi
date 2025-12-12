from typing import Any

from invenio_jobs.jobs import JobType
from invenio_vocabularies.contrib.names.datastreams import (
    ORCID_PRESET_DATASTREAM_CONFIG as ORCID_PRESET_DATASTREAM_CONFIG,
)
from invenio_vocabularies.services.tasks import process_datastream as process_datastream

class ProcessDataStreamJob(JobType):
    task = process_datastream

class ProcessRORAffiliationsJob(ProcessDataStreamJob):
    description: Any
    title: Any
    id: str
    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs) -> dict[str, Any]: ...

class ProcessRORFundersJob(ProcessDataStreamJob):
    description: Any
    title: Any
    id: str
    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs) -> dict[str, Any]: ...

class ImportAwardsOpenAIREJob(ProcessDataStreamJob):
    description: Any
    title: Any
    id: str
    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs) -> dict[str, Any]: ...

class UpdateAwardsCordisJob(ProcessDataStreamJob):
    description: Any
    title: Any
    id: str
    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs) -> dict[str, Any]: ...

class ImportORCIDJob(ProcessDataStreamJob):
    description: Any
    title: Any
    id: str
    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs) -> dict[str, Any]: ...
