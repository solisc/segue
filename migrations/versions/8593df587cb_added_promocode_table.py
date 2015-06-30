"""added_promocode_table

Revision ID: 8593df587cb
Revises: 11dd09c50161
Create Date: 2015-06-30 19:10:30.629792

"""

# revision identifiers, used by Alembic.
revision = '8593df587cb'
down_revision = '11dd09c50161'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promo_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('hash_code', sa.String(length=32), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column(u'product', 'is_promo')
    op.drop_column(u'product', 'is_speaker')
    op.drop_column(u'product', 'gives_kit')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'product', sa.Column('gives_kit', sa.BOOLEAN(), server_default=sa.text(u'true'), autoincrement=False, nullable=True))
    op.add_column(u'product', sa.Column('is_speaker', sa.BOOLEAN(), server_default=sa.text(u'false'), autoincrement=False, nullable=True))
    op.add_column(u'product', sa.Column('is_promo', sa.BOOLEAN(), server_default=sa.text(u'false'), autoincrement=False, nullable=True))
    op.drop_table('promo_code')
    ### end Alembic commands ###