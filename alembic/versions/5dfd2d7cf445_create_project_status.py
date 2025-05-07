"""Create Project Status

Revision ID: 5dfd2d7cf445
Revises: b633751603d6
Create Date: 2025-05-07 14:54:01.022790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dfd2d7cf445'
down_revision = 'b633751603d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('project_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_status_name'), 'project_status', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_project_status_name'), table_name='project_status')
    op.drop_table('project_status')
