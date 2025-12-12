from invenio_records_resources.resources.records.args import SearchRequestArgsSchema
from marshmallow import fields

class CommunitiesSearchRequestArgsSchema(SearchRequestArgsSchema):
    status: fields.Str
    include_deleted: fields.Bool
