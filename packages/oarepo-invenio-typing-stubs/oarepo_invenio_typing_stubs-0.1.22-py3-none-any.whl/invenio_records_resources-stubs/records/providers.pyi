from typing import Any

from invenio_records_resources.records.api import Record

class ModelPIDProvider:
    @classmethod
    def create(
        cls,
        pid_value: str,
        record: Record,
        model_field_name: str,
        **kwargs: Any,
    ) -> None: ...
