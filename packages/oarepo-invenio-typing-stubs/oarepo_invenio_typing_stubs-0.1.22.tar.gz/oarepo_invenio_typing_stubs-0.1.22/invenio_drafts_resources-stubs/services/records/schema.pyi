from _typeshed import Incomplete
from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema

class VersionsSchema(Schema):
    is_latest: Incomplete
    is_latest_draft: Incomplete
    index: Incomplete

class ParentSchema(Schema):
    id: Incomplete

class RecordSchema(BaseRecordSchema):
    parent: Incomplete
    versions: Incomplete
    is_published: Incomplete
    is_draft: Incomplete
    expires_at: Incomplete
