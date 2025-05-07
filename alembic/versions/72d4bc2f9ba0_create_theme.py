"""Create Theme

Revision ID: 72d4bc2f9ba0
Revises: 3b18c7f53fa5
Create Date: 2025-05-07 14:56:40.466532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72d4bc2f9ba0'
down_revision = '3b18c7f53fa5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('theme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_theme_name'), 'theme', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_theme_name'), table_name='theme')
    op.drop_table('theme')
