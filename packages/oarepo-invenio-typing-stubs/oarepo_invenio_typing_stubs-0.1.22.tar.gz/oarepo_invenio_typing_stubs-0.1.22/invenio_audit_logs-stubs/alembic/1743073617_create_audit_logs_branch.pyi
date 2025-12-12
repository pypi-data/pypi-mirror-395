# Stub for alembic migration: create audit logs branch

revision: str
down_revision: None | str
branch_labels: tuple[str, ...]
depends_on: None | str

def upgrade() -> None: ...
def downgrade() -> None: ...
