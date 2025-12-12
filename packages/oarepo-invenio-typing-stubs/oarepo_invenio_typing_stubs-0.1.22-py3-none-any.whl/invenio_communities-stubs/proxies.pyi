from invenio_communities.cache.cache import IdentityCache
from invenio_communities.ext import InvenioCommunities
from invenio_communities.roles import RoleRegistry as RoleRegistry

current_communities: InvenioCommunities  # intentionally not LazyProxy
current_roles: RoleRegistry  # intentionally not LazyProxy
current_identities_cache: IdentityCache  # intentionally not LazyProxy
