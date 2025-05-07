"""Create Methodology

Revision ID: 92de6eedf921
Revises: 06b056f8efd7
Create Date: 2025-05-07 14:52:28.169979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92de6eedf921'
down_revision = '06b056f8efd7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('methodology',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_methodology_name'), 'methodology', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_methodology_name'), table_name='methodology')
    op.drop_table('methodology')
