"""new_update_2

Revision ID: b52ddd460fb3
Revises: cd586b24a779
Create Date: 2023-10-23 13:30:55.219598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b52ddd460fb3'
down_revision = 'cd586b24a779'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_task')
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
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('project_id')
        batch_op.drop_column('status_id')

    op.create_table('_alembic_tmp_task',
    sa.Column('task_id', sa.INTEGER(), nullable=False),
    sa.Column('status_id', sa.INTEGER(), nullable=False),
    sa.Column('project_id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('priority_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['priority_id'], ['priority.priority_id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], name='fk_tasks_projects'),
    sa.ForeignKeyConstraint(['status_id'], ['status.status_id'], name='fk_tasks_status'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('task_id')
    )
    # ### end Alembic commands ###