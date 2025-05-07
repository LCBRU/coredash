"""Create Research Type

Revision ID: 376374663d3b
Revises: 090054938053
Create Date: 2025-05-07 14:55:29.666784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '376374663d3b'
down_revision = '090054938053'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('research_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_research_type_name'), 'research_type', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_research_type_name'), table_name='research_type')
    op.drop_table('research_type')
