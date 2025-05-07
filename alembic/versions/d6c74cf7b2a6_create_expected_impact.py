"""Create Expected Impact

Revision ID: d6c74cf7b2a6
Revises:
Create Date: 2025-05-07 14:46:43.571706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6c74cf7b2a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('expected_impact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_expected_impact_name'), 'expected_impact', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_expected_impact_name'), table_name='expected_impact')
    op.drop_table('expected_impact')
