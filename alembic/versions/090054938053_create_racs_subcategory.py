"""Create RACS SubCategory

Revision ID: 090054938053
Revises: 5dfd2d7cf445
Create Date: 2025-05-07 14:54:46.421310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '090054938053'
down_revision = '5dfd2d7cf445'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('racs_sub_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_racs_sub_category_name'), 'racs_sub_category', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_racs_sub_category_name'), table_name='racs_sub_category')
    op.drop_table('racs_sub_category')
