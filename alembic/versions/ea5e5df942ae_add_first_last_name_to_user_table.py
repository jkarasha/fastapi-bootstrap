"""add_first_last_name_to_user_table

Revision ID: ea5e5df942ae
Revises: 7bb2856f3752
Create Date: 2025-01-25 20:02:20.911374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea5e5df942ae'
down_revision: Union[str, None] = '7bb2856f3752'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
