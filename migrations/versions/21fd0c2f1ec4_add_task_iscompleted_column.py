"""add task isCompleted column

Revision ID: 21fd0c2f1ec4
Revises: da40fbcbf6ca
Create Date: 2023-10-09 14:46:11.562923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21fd0c2f1ec4'
down_revision = 'da40fbcbf6ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isCompleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('isCompleted')

    # ### end Alembic commands ###
