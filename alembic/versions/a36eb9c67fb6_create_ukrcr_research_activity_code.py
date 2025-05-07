"""Create UKRCR Research Activity Code

Revision ID: a36eb9c67fb6
Revises: a75a656e94d7
Create Date: 2025-05-07 14:59:11.317011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a36eb9c67fb6'
down_revision = 'a75a656e94d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('ukcrc_research_activity_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ukcrc_research_activity_code_name'), 'ukcrc_research_activity_code', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_ukcrc_research_activity_code_name'), table_name='ukcrc_research_activity_code')
    op.drop_table('ukcrc_research_activity_code')
