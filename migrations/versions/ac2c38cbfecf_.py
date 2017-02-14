"""empty message

Revision ID: ac2c38cbfecf
Revises: c710d6134c42
Create Date: 2017-02-14 00:54:52.693000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac2c38cbfecf'
down_revision = 'c710d6134c42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=56), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token')
    # ### end Alembic commands ###