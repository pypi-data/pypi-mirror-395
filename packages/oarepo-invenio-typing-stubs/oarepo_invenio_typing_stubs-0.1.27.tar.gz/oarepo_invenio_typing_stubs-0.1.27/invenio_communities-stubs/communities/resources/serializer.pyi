from flask_resources import MarshmallowSerializer
from invenio_communities.communities.resources.ui_schema import UICommunitySchema as UICommunitySchema

class UICommunityJSONSerializer(MarshmallowSerializer):
    def __init__(self) -> None: ...
