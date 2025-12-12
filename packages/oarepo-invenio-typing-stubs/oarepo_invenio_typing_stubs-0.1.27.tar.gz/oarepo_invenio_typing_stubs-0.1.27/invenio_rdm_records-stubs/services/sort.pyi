from invenio_records_resources.services.records.params.sort import SortParam

class VerifiedRecordsSortParam(SortParam):
    def apply(self, identity, search, params): ...
