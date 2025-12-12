from typing import Any, Dict, List

from flask_principal import Identity
from flask_resources import BaseObjectSchema
from invenio_communities.communities.schema import (
    CommunityThemeSchema as CommunityThemeSchema,
)
from invenio_communities.proxies import current_communities as current_communities
from marshmallow import Schema, fields

def mask_removed_by(obj): ...
def _community_permission_check(
    action: str, community: Dict[str, Any], identity: Identity
) -> bool: ...

FormatEDTF: Any

class TombstoneSchema(Schema):
    removal_reason: fields.Nested
    note: fields.Str
    removed_by: fields.Function
    removal_date_l10n_medium: Any
    removal_date_l10n_long: Any
    citation_text: fields.Str
    is_visible: fields.Bool

class FundingSchema(Schema):
    award: fields.Nested
    funder: fields.Nested

class UICommunitySchema(BaseObjectSchema):
    type: fields.Nested
    funding: fields.List
    tombstone: fields.Nested
    organizations: fields.Method
    theme: fields.Nested
    custom_fields: fields.Nested
    permissions: fields.Method
    def get_organizations(self, obj: Dict[str, Any]) -> List[Any]: ...
    def get_permissions(self, obj: Dict[str, Any]) -> Dict[str, bool]: ...
    def post_dump(
        self, data: Dict[str, Any], original: Dict[str, Any], many: bool, **kwargs: Any
    ) -> Dict[str, Any]: ...

class TypesSchema(Schema):
    types: fields.List
