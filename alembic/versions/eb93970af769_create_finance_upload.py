"""Create Finance Upload

Revision ID: eb93970af769
Revises: d6c74cf7b2a6
Create Date: 2025-05-07 14:47:47.336279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb93970af769'
down_revision = 'd6c74cf7b2a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('finance_upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('guid', sa.String(length=50), nullable=False),
    sa.Column('filename', sa.String(length=500), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('finance_upload')
