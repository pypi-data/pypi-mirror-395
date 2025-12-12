"""Add trade_group_id, openDate and closeDate to trades table

Revision ID: a1b2c3d4e5f6
Revises: cc3c6f4d83dc
Create Date: 2025-10-23 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'cc3c6f4d83dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add trade_group_id, openDate and closeDate columns to trades table"""
    # Add trade_group_id column (nullable, for grouping related trades like rollovers)
    op.add_column('trades', sa.Column('trade_group_id', sa.String(), nullable=True))
    
    # Add openDate column (nullable, timestamp when trade was opened)
    op.add_column('trades', sa.Column('openDate', sa.TIMESTAMP(), nullable=True))
    
    # Add closeDate column (nullable, timestamp when trade was closed)
    op.add_column('trades', sa.Column('closeDate', sa.TIMESTAMP(), nullable=True))
    
    # Migrate existing trade data: Set openDate and closeDate based on transactions
    connection = op.get_bind()
    
    # Update openDate: Set to timestamp of first transaction (MIN)
    connection.execute(sa.text("""
        UPDATE trades
        SET openDate = (
            SELECT MIN(timestamp)
            FROM transactions
            WHERE transactions.tradeid = trades.id
        )
        WHERE EXISTS (
            SELECT 1 FROM transactions WHERE transactions.tradeid = trades.id
        )
    """))
    
    # Update closeDate: Set to timestamp of last transaction (MAX), only for CLOSED trades
    connection.execute(sa.text("""
        UPDATE trades
        SET closeDate = (
            SELECT MAX(timestamp)
            FROM transactions
            WHERE transactions.tradeid = trades.id
        )
        WHERE status = 'CLOSED'
        AND EXISTS (
            SELECT 1 FROM transactions WHERE transactions.tradeid = trades.id
        )
    """))


def downgrade() -> None:
    """Remove trade_group_id, openDate and closeDate columns from trades table"""
    op.drop_column('trades', 'closeDate')
    op.drop_column('trades', 'openDate')
    op.drop_column('trades', 'trade_group_id')
