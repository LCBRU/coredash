"""Create Job Title

Revision ID: d7a8679a42bc
Revises: 9f86d663257a
Create Date: 2025-05-16 14:25:53.491628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7a8679a42bc'
down_revision = '9f86d663257a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('job_title',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_title_name'), 'job_title', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_job_title_name'), table_name='job_title')
    op.drop_table('job_title')
