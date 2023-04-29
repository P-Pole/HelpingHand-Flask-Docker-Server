"""Added columns

Revision ID: 4f43c995fe76
Revises: 256321843f82
Create Date: 2023-04-27 09:19:54.908575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f43c995fe76'
down_revision = '256321843f82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('subscription', sa.Boolean(), nullable=True))
    op.add_column('transactions', sa.Column('amount', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'amount')
    op.drop_column('transactions', 'subscription')
    # ### end Alembic commands ###