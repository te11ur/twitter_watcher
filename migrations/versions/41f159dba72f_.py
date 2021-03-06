"""empty message

Revision ID: 41f159dba72f
Revises: 74a761540b13
Create Date: 2017-02-06 00:52:16.045000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41f159dba72f'
down_revision = '74a761540b13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('repository', sa.Column('key', sa.String(length=90), nullable=True))
    op.add_column('watcher', sa.Column('name', sa.String(length=100), nullable=True))
    op.drop_column('watcher', 'indexer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('watcher', sa.Column('indexer', sa.VARCHAR(length=90), autoincrement=False, nullable=True))
    op.drop_column('watcher', 'name')
    op.drop_column('repository', 'key')
    # ### end Alembic commands ###
