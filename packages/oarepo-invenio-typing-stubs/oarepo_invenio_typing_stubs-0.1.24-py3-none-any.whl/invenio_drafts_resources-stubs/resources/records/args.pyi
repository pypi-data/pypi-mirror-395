from invenio_records_resources.resources.records.args import (
    SearchRequestArgsSchema as SearchRequestArgsSchemaBase,
)
from marshmallow import fields

class SearchRequestArgsSchema(SearchRequestArgsSchemaBase):
    allversions: fields.Boolean
    include_deleted: fields.Boolean
