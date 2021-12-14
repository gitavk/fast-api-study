"""Create users table

Revision ID: 59d933c9958c
Revises: 5a3c19386396
Create Date: 2021-12-13 22:09:23.145888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59d933c9958c"
down_revision = "5a3c19386396"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("pk", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("email"),
    )


def downgrade():
    op.drop_table("users")
