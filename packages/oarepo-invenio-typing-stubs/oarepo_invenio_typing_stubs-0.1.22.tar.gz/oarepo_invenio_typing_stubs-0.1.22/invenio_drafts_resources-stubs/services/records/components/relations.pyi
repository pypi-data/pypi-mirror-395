from invenio_records_resources.services.records.components import RelationsComponent as RelationsComponentBase

class RelationsComponent(RelationsComponentBase):
    def read_draft(self, identity, draft=None, errors=None) -> None: ...
