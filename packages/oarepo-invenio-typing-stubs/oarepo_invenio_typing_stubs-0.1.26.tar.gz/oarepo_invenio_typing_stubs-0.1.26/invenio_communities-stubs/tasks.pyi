from celery import shared_task
from invenio_communities.proxies import current_identities_cache as current_identities_cache

@shared_task
def clear_cache() -> None: ...
