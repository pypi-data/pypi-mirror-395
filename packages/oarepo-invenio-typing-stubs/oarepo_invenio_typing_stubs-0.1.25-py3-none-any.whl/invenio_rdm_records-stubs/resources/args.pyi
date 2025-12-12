from invenio_drafts_resources.resources.records.args import SearchRequestArgsSchema
from marshmallow import fields

class RDMSearchRequestArgsSchema(SearchRequestArgsSchema):
    style: fields.Str
    locale: fields.Str
    status: fields.Str
    include_deleted: fields.Bool
    shared_with_me: fields.Bool
