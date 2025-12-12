from collections.abc import Mapping

from invenio_drafts_resources.resources.records.args import (
    SearchRequestArgsSchema as SearchRequestArgsSchema,
)
from invenio_records_resources.resources import (
    RecordResourceConfig as RecordResourceConfigBase,
)
from invenio_records_resources.resources.records.args import (
    SearchRequestArgsSchema as BaseSearchRequestArgsSchema,
)

class RecordResourceConfig(RecordResourceConfigBase):
    # NOTE: configs expose immutable defaults so subclass overrides don't
    # mutate shared state.
    url_prefix: str | None
    routes: Mapping[str, str]
    request_search_args: type[BaseSearchRequestArgsSchema]
