"""Create UKRCR Health Category

Revision ID: a75a656e94d7
Revises: 5d47b0b67ba9
Create Date: 2025-05-07 14:58:11.559622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a75a656e94d7'
down_revision = '5d47b0b67ba9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('ukcrc_health_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ukcrc_health_category_name'), 'ukcrc_health_category', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_ukcrc_health_category_name'), table_name='ukcrc_health_category')
    op.drop_table('ukcrc_health_category')
