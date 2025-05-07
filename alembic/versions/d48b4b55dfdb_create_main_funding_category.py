"""Create Main Funding Category

Revision ID: d48b4b55dfdb
Revises: eb93970af769
Create Date: 2025-05-07 14:48:39.007290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd48b4b55dfdb'
down_revision = 'eb93970af769'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('main_funding_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_main_funding_category_name'), 'main_funding_category', ['name'], unique=True)



def downgrade() -> None:
    op.drop_index(op.f('ix_main_funding_category_name'), table_name='main_funding_category')
    op.drop_table('main_funding_category')
