"""add user_book abd upgrade transaction

Revision ID: e3b6c6d90c01
Revises: ee799c5aab9b
Create Date: 2024-12-22 13:33:13.028433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3b6c6d90c01'
down_revision: Union[str, None] = 'ee799c5aab9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('card_num', sa.String(length=225), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'card_num')
    # ### end Alembic commands ###