"""empty message

Revision ID: 975a59afdd9f
Revises: 18e746c410e0
Create Date: 2017-02-09 12:39:54.803014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '975a59afdd9f'
down_revision = '18e746c410e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('service', 'api',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('service', 'api',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###
