"""Create Role

Revision ID: 3b18c7f53fa5
Revises: 376374663d3b
Create Date: 2025-05-07 14:56:05.096677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b18c7f53fa5'
down_revision = '376374663d3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )


def downgrade() -> None:
    op.drop_table('role')
