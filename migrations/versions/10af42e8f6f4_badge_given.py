"""badge given column

Revision ID: 10af42e8f6f4
Revises: 1fc7d636675a
Create Date: 2015-07-06 21:43:18.812394

"""

# revision identifiers, used by Alembic.
revision = '10af42e8f6f4'
down_revision = '1fc7d636675a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('badge', sa.Column('given', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('badge', 'given')
    ### end Alembic commands ###
