"""initial migration: create users and tweets tables

Revision ID: 24ca1e7849f0
Revises:
Create Date: 2026-01-06 21:49:01.426764

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "24ca1e7849f0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True, index=True),
        sa.Column("email", sa.String(100), nullable=False, unique=True, index=True),
        sa.Column("full_name", sa.String(100), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("followers_count", sa.Integer(), nullable=False, default=0),
        sa.Column("following_count", sa.Integer(), nullable=False, default=0),
    )

    # Create tweets table
    op.create_table(
        "tweets",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("content", sa.String(280), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("likes_count", sa.Integer(), nullable=False, default=0),
        sa.Column("retweets_count", sa.Integer(), nullable=False, default=0),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tweets")
    op.drop_table("users")
