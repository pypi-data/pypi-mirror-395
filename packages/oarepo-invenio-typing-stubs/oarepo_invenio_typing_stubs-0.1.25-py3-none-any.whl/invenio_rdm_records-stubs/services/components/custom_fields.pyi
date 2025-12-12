from invenio_rdm_records.services.components.metadata import MetadataComponent

class CustomFieldsComponent(MetadataComponent):
    field: str
    new_version_skip_fields: list[str]
