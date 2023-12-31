"""new_update_3

Revision ID: e36576b1197d
Revises: b52ddd460fb3
Create Date: 2023-10-23 13:33:14.379806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e36576b1197d'
down_revision = 'b52ddd460fb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('project_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_tasks_status'), 'status', ['status_id'], ['status_id'])
        batch_op.create_foreign_key(batch_op.f('fk_tasks_projects'), 'projects', ['project_id'], ['project_id'])
        batch_op.drop_column('isCompleted')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isCompleted', sa.BOOLEAN(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_tasks_status'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_tasks_projects'), type_='foreignkey')
        batch_op.drop_column('project_id')
        batch_op.drop_column('status_id')

    # ### end Alembic commands ###
