from typing import List

from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import Generator
from invenio_vocabularies.services.generators import IfTags as IfTags

class PermissionPolicy(RecordPermissionPolicy):
    can_list_vocabularies: List[Generator] | tuple[Generator, ...]
