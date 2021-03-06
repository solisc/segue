"""added a column for caravan description

Revision ID: 2624c849d8be
Revises: 309fd98acc42
Create Date: 2015-04-11 20:17:10.377106

"""

# revision identifiers, used by Alembic.
revision = '2624c849d8be'
down_revision = '309fd98acc42'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('caravan', sa.Column('description', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('caravan', 'description')
    ### end Alembic commands ###
