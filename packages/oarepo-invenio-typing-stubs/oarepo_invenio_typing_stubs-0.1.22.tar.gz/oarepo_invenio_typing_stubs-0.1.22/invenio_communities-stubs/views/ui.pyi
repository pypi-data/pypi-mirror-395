from flask.app import Flask
from flask.blueprints import Blueprint
from invenio_communities.communities.resources.serializer import (
    UICommunityJSONSerializer as UICommunityJSONSerializer,
)
from invenio_communities.errors import CommunityDeletedError as CommunityDeletedError
from invenio_communities.errors import LogoNotFoundError as LogoNotFoundError
from invenio_communities.proxies import current_communities as current_communities
from invenio_communities.searchapp import search_app_context as search_app_context
from invenio_communities.views.communities import (
    communities_about as communities_about,
)
from invenio_communities.views.communities import (
    communities_curation_policy as communities_curation_policy,
)
from invenio_communities.views.communities import (
    communities_frontpage as communities_frontpage,
)
from invenio_communities.views.communities import (
    communities_new as communities_new,
)
from invenio_communities.views.communities import (
    communities_new_subcommunity as communities_new_subcommunity,
)
from invenio_communities.views.communities import (
    communities_requests as communities_requests,
)
from invenio_communities.views.communities import (
    communities_search as communities_search,
)
from invenio_communities.views.communities import (
    communities_settings as communities_settings,
)
from invenio_communities.views.communities import (
    communities_settings_pages as communities_settings_pages,
)
from invenio_communities.views.communities import (
    communities_settings_privileges as communities_settings_privileges,
)
from invenio_communities.views.communities import (
    communities_settings_submission_policy as communities_settings_submission_policy,
)
from invenio_communities.views.communities import (
    communities_subcommunities as communities_subcommunities,
)
from invenio_communities.views.communities import (
    community_theme_css_config as community_theme_css_config,
)
from invenio_communities.views.communities import invitations as invitations
from invenio_communities.views.communities import members as members
from invenio_communities.views.decorators import warn_deprecation as warn_deprecation

def not_found_error(error): ...
def record_tombstone_error(error): ...
def record_permission_denied_error(error): ...
def create_ui_blueprint(app: Flask) -> Blueprint: ...
