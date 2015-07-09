"""adds a hash_code column to purchase table

Revision ID: 50726805d9a6
Revises: 34d7989605a9
Create Date: 2015-07-06 04:10:52.399737

"""

# revision identifiers, used by Alembic.
revision = '50726805d9a6'
down_revision = '34d7989605a9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchase', sa.Column('hash_code', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchase', 'hash_code')
    ### end Alembic commands ###