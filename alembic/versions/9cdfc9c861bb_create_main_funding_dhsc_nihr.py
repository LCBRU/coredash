"""Create Main Funding DHSC NIHR

Revision ID: 9cdfc9c861bb
Revises: d48b4b55dfdb
Create Date: 2025-05-07 14:49:52.871313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cdfc9c861bb'
down_revision = 'd48b4b55dfdb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('main_funding_dhsc_nihr_funding',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_main_funding_dhsc_nihr_funding_name'), 'main_funding_dhsc_nihr_funding', ['name'], unique=True)



def downgrade() -> None:
    op.drop_index(op.f('ix_main_funding_dhsc_nihr_funding_name'), table_name='main_funding_dhsc_nihr_funding')
    op.drop_table('main_funding_dhsc_nihr_funding')

