from typing import Any

from invenio_records_resources.services.records.params.base import ParamInterpreter


class StatusParam(ParamInterpreter):
    def apply(self, identity, search, params: dict[str, Any]): ...


class PublishedRecordsParam(ParamInterpreter):
    def apply(self, identity, search, params: dict[str, Any]): ...


class SharedOrMyDraftsParam(ParamInterpreter):
    def _generate_shared_with_me_query(self, identity) -> Any: ...
    def apply(self, identity, search, params: dict[str, Any]): ...


class MetricsParam(ParamInterpreter):
    def apply(self, identity, search, params: dict[str, Any]): ...
