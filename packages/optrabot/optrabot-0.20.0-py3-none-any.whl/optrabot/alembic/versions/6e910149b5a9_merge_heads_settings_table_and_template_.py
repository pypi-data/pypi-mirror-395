"""merge heads: settings table and template_name

Revision ID: 6e910149b5a9
Revises: fca33d484976, b2c3d4e5f6g7
Create Date: 2025-10-27 12:05:20.371245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e910149b5a9'
down_revision: Union[str, None] = ('fca33d484976', 'b2c3d4e5f6g7')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
