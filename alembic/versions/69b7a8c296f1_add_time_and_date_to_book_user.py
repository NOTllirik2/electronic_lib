"""add time and date to book_user

Revision ID: 69b7a8c296f1
Revises: e3b6c6d90c01
Create Date: 2024-12-22 18:16:57.175201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69b7a8c296f1'
down_revision: Union[str, None] = 'e3b6c6d90c01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_book', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('user_book', sa.Column('time', sa.Date(), nullable=False))
    op.drop_column('user_book', 'purchase_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_book', sa.Column('purchase_date', sa.DATE(), nullable=False))
    op.drop_column('user_book', 'time')
    op.drop_column('user_book', 'date')
    # ### end Alembic commands ###
