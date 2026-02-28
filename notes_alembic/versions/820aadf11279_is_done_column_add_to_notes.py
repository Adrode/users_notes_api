"""is_done column add to notes

Revision ID: 820aadf11279
Revises: 62a9485ee6cc
Create Date: 2026-02-25 20:46:20.900325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '820aadf11279'
down_revision: Union[str, Sequence[str], None] = '62a9485ee6cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('notes', sa.Column('is_done', sa.Boolean(), nullable=True))
    op.alter_column('notes', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

def downgrade() -> None:
    op.alter_column('notes', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('notes', 'is_done')