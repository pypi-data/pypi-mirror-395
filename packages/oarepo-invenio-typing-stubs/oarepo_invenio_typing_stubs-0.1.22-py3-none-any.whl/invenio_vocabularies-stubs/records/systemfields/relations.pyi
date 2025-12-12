from invenio_records.systemfields import RelationsField
from invenio_vocabularies.records.api import Vocabulary as Vocabulary

class CustomFieldsRelation(RelationsField):
    def __init__(self, fields_var) -> None: ...
