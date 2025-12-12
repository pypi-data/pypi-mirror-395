from click import Command, Context, Group, Parameter
from sqlalchemy.engine import URL

def abort_if_false(ctx: Context, param: Parameter, value: bool) -> None: ...
def render_url(url: URL) -> str: ...

# click command group and commands
db: Group
create: Command
drop: Command
init: Command
destroy: Command
