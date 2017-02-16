"""empty message

Revision ID: fec41e18e4e4
Revises: ac2c38cbfecf
Create Date: 2017-02-16 11:07:45.960351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fec41e18e4e4'
down_revision = 'ac2c38cbfecf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('watcher', sa.Column('push_params', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('watcher', 'push_params')
    # ### end Alembic commands ###
