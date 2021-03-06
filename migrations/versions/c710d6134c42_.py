"""empty message

Revision ID: c710d6134c42
Revises: e63c207a6ded
Create Date: 2017-02-11 15:20:31.173000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c710d6134c42'
down_revision = 'e63c207a6ded'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service', 'push')
    op.drop_column('service', 'enabled')
    op.drop_column('service', 'repository')
    op.add_column('watcher', sa.Column('push', sa.Boolean(), nullable=True))
    op.add_column('watcher', sa.Column('repository', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('watcher', 'repository')
    op.drop_column('watcher', 'push')
    op.add_column('service', sa.Column('repository', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('service', sa.Column('enabled', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('service', sa.Column('push', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
