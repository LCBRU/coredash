"""Create Main Funding Source

Revision ID: 06b056f8efd7
Revises: 4aaf68fba825
Create Date: 2025-05-07 14:51:25.462053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06b056f8efd7'
down_revision = '4aaf68fba825'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('main_funding_source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_main_funding_source_name'), 'main_funding_source', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_main_funding_source_name'), table_name='main_funding_source')
    op.drop_table('main_funding_source')
