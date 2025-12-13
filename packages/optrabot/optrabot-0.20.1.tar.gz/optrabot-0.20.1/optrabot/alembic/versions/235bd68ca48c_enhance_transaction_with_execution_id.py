"""Enhance transaction with execution id

Revision ID: 235bd68ca48c
Revises: 6e910149b5a9
Create Date: 2025-11-12 13:07:13.702780

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '235bd68ca48c'
down_revision: Union[str, None] = '6e910149b5a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add exec_id column to transactions table
    op.add_column('transactions', sa.Column('exec_id', sa.String(), nullable=True))

def downgrade() -> None:
    # Remove exec_id column from transactions table
    op.drop_column('transactions', 'exec_id')
