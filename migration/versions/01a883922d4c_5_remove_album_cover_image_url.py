"""5. remove album cover image url

Revision ID: 01a883922d4c
Revises: 2cf20b052545
Create Date: 2023-08-12 11:57:40.157886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '01a883922d4c'
down_revision: Union[str, None] = '2cf20b052545'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('albums', 'cover_image_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albums', sa.Column('cover_image_url', mysql.VARCHAR(length=255), nullable=True))
    # ### end Alembic commands ###