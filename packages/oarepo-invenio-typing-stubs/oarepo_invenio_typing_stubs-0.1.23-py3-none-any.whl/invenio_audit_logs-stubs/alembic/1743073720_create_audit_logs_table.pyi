# Stub for alembic migration: create audit logs table

revision: str
down_revision: None | str
branch_labels: tuple[()] | tuple[str, ...]
depends_on: None | str

def upgrade() -> None: ...
def downgrade() -> None: ...
