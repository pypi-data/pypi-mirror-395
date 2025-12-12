from typing import Any, Callable, TypeVar

from click import Command, Group

F = TypeVar("F", bound=Callable[..., Any])

def abort_if_false(ctx: Any, param: Any, value: Any) -> None: ...
def search_version_check(f: F) -> F: ...

# Click group and commands
index: Group
check: Command
init: Command
destroy: Command
create: Command
update: Command
list_cmd: Command
delete: Command
put: Command
