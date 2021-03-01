"""Add api_client table

Revision ID: 073cc958abf2
Revises: 20f05b0d3dc8
Create Date: 2021-03-03 22:02:48.959788

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "073cc958abf2"  # pragma: allowlist secret
down_revision = "20f05b0d3dc8"  # pragma: allowlist secret
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "api_client",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.Column("hashed_secret", sa.String(), nullable=False),
        sa.Column(
            "create_timestamp",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_timestamp",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("name"),
    )


def downgrade():
    op.drop_table("api_client")
