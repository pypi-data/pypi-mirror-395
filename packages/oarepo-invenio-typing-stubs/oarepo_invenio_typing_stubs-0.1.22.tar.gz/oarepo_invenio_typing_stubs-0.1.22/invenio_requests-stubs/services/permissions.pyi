from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import Generator
from invenio_requests.services.generators import Commenter as Commenter
from invenio_requests.services.generators import Creator as Creator
from invenio_requests.services.generators import Receiver as Receiver
from invenio_requests.services.generators import Reviewers as Reviewers
from invenio_requests.services.generators import Status as Status
from invenio_requests.services.generators import Topic as Topic

class PermissionPolicy(RecordPermissionPolicy):
    # NOTE: tuples keep these generator lists immutable on the base class while
    # enabling subclasses to override with their own tuples of generators.
    can_create: tuple[Generator, ...]
    can_search: tuple[Generator, ...]
    can_search_user_requests = can_search
    can_read: tuple[Generator, ...]
    can_update: tuple[Generator, ...]
    can_manage_access_options: tuple[Generator, ...]
    can_action_delete: tuple[Generator, ...]
    can_action_submit: tuple[Generator, ...]
    can_action_cancel: tuple[Generator, ...]
    can_action_expire: tuple[Generator, ...]
    can_action_accept: tuple[Generator, ...]
    can_action_decline: tuple[Generator, ...]
    can_update_comment: tuple[Generator, ...]
    can_delete_comment: tuple[Generator, ...]
    can_create_comment: tuple[Generator, ...]
    can_unused: tuple[Generator, ...]
