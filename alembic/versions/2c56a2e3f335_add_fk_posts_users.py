"""Add FK posts-users

Revision ID: 2c56a2e3f335
Revises: 59d933c9958c
Create Date: 2021-12-13 22:19:33.787149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2c56a2e3f335"
down_revision = "59d933c9958c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        "fk_posts_users",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["pk"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_column("posts", "owner_id")
