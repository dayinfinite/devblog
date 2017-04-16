"""empty message

Revision ID: eb0563ba4383
Revises: e261e9e342c2
Create Date: 2017-04-17 01:49:10.205000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb0563ba4383'
down_revision = 'e261e9e342c2'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password_hash')
    ### end Alembic commands ###
