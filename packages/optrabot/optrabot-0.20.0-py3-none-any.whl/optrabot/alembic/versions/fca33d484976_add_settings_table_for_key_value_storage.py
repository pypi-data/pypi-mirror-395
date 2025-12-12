"""Add settings table for key-value storage

Revision ID: fca33d484976
Revises: a1b2c3d4e5f6
Create Date: 2025-10-24 08:23:56.166732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fca33d484976'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create settings table for key-value storage"""
    op.create_table(
        'settings',
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('value', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('key')
    )


def downgrade() -> None:
    """Drop settings table"""
    op.drop_table('settings')

