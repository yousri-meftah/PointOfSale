"""relation between order and program_item

Revision ID: 0d94a7ff6e09
Revises: 78861cb8e10e
Create Date: 2024-07-17 14:10:10.091968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d94a7ff6e09'
down_revision: Union[str, None] = '78861cb8e10e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'order', 'program_item', ['program_item_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    # ### end Alembic commands ###
