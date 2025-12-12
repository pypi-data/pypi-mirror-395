import click
from invenio_communities.fixtures.demo import (
    create_fake_community as create_fake_community,
)
from invenio_communities.fixtures.tasks import (
    create_demo_community as create_demo_community,
)
from invenio_communities.proxies import (
    current_communities as current_communities,
)
from invenio_communities.proxies import (
    current_identities_cache as current_identities_cache,
)

# keep typing of these objects. They are functions but at the same time click commands/groups
communities: click.Group
identity_cache: click.Group
clear: click.Command
demo: click.Command
rebuild_index: click.Command
custom_fields: click.Group
create_communities_custom_field: click.Command
custom_field_exists_in_communities: click.Command
