from invenio_rdm_records.services.errors import RDMRecordsException

class PIDSchemeNotSupportedError(RDMRecordsException):
    def __init__(self, schemes: set[str]) -> None: ...

class ProviderNotSupportedError(RDMRecordsException):
    def __init__(self, provider: str, scheme: str) -> None: ...
