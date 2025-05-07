"""Create Trial Phase

Revision ID: 5d47b0b67ba9
Revises: 72d4bc2f9ba0
Create Date: 2025-05-07 14:57:20.158856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d47b0b67ba9'
down_revision = '72d4bc2f9ba0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('trial_phase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trial_phase_name'), 'trial_phase', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_trial_phase_name'), table_name='trial_phase')
    op.drop_table('trial_phase')
