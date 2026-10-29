"""Merge the two existing migration branches."""

revision = "merge_heads"
down_revision = ("0002_run_duration_index", "605f620a49af")
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
