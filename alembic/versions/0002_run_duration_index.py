"""Ensure report duration and activity lookup indexes exist."""
from alembic import op
import sqlalchemy as sa

revision = "0002_run_duration_index"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    # run_duration_seconds is included in the initial model for fresh installs.
    # Create the index only if it does not already exist in the current database.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    indexes = {i["name"] for i in inspector.get_indexes("report_activity")}
    if "ix_activity_status_created" not in indexes:
        op.create_index("ix_activity_status_created", "report_activity", ["status", "created_at"], unique=False)

def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    indexes = {i["name"] for i in inspector.get_indexes("report_activity")}
    if "ix_activity_status_created" in indexes:
        op.drop_index("ix_activity_status_created", table_name="report_activity")
