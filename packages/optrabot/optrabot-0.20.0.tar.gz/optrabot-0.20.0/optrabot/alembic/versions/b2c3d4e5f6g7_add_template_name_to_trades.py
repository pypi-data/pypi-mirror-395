"""Add template_name to trades table for trade recovery

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2025-10-27 10:00:00.000000

OTB-253 Phase 2: Store template name to enable active trade recovery
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6g7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add template_name column to trades table
    
    This allows us to:
    - Identify which template was used to create a trade
    - Recover active trades after OptraBot restart
    - Match trades to their original templates for monitoring
    """
    # Add template_name column (nullable for backward compatibility)
    op.add_column('trades', sa.Column('template_name', sa.String(), nullable=True))
    
    # Note: Existing trades will have template_name = NULL
    # This is acceptable - only new trades need template_name for recovery


def downgrade() -> None:
    """Remove template_name column from trades table"""
    op.drop_column('trades', 'template_name')
