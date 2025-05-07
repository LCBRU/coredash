"""Create NIHR Priority Area

Revision ID: b633751603d6
Revises: 92de6eedf921
Create Date: 2025-05-07 14:53:15.804445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b633751603d6'
down_revision = '92de6eedf921'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('nihr_priority_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nihr_priority_area_name'), 'nihr_priority_area', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_nihr_priority_area_name'), table_name='nihr_priority_area')
    op.drop_table('nihr_priority_area')
