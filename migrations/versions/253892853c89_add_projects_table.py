"""add projects table

Revision ID: 253892853c89
Revises: 7cad89652a9a
Create Date: 2023-10-23 13:17:52.544459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '253892853c89'
down_revision = '7cad89652a9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status',
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('desc', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('status_id')
    )
    op.create_table('projects',
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('desc', sa.String(length=255), nullable=False),
    sa.Column('deadline', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['status_id'], ['status.status_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('project_id')
    )
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('project_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'projects', ['project_id'], ['project_id'])
        batch_op.create_foreign_key(None, 'status', ['status_id'], ['status_id'])
        batch_op.drop_column('isCompleted')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isCompleted', sa.BOOLEAN(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('project_id')
        batch_op.drop_column('status_id')

    op.drop_table('projects')
    op.drop_table('status')
    # ### end Alembic commands ###
