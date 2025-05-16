"""Create ProfessionalBackghround

Revision ID: 96f9688c93bb
Revises: d7a8679a42bc
Create Date: 2025-05-16 14:36:36.117557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96f9688c93bb'
down_revision = 'd7a8679a42bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('professional_background',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_professional_background_name'), 'professional_background', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_professional_background_name'), table_name='professional_background')
    op.drop_table('professional_background')
