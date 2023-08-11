"""3. add artist gender

Revision ID: 99c1cd43688e
Revises: 23a75af772b7
Create Date: 2023-08-11 17:02:22.391171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99c1cd43688e'
down_revision: Union[str, None] = '23a75af772b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'UNDEFINED', name='gender'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'gender')
    # ### end Alembic commands ###
