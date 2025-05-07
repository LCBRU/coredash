"""Create Main Funding Industry

Revision ID: 4aaf68fba825
Revises: 9cdfc9c861bb
Create Date: 2025-05-07 14:50:41.197792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aaf68fba825'
down_revision = '9cdfc9c861bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('main_funding_industry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_main_funding_industry_name'), 'main_funding_industry', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_main_funding_industry_name'), table_name='main_funding_industry')
    op.drop_table('main_funding_industry')
