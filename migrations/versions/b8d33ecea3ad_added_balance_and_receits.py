"""Added balance and receits 

Revision ID: b8d33ecea3ad
Revises: 5af96ef2ce96
Create Date: 2025-02-17 02:47:51.349696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8d33ecea3ad'
down_revision = '5af96ef2ce96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('receipt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('purchase_date', sa.DateTime(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['buyer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('pending_balance', sa.Float(), nullable=True))

    with op.batch_alter_table('vendors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('pending_balance', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vendors', schema=None) as batch_op:
        batch_op.drop_column('pending_balance')
        batch_op.drop_column('balance')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('pending_balance')
        batch_op.drop_column('balance')

    op.drop_table('receipt')
    # ### end Alembic commands ###
