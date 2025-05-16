"""Create ProfessionalBackghroundDetails

Revision ID: 1aa88ce89b93
Revises: 96f9688c93bb
Create Date: 2025-05-16 14:37:18.645390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aa88ce89b93'
down_revision = '96f9688c93bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('professional_background_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_professional_background_detail_name'), 'professional_background_detail', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_professional_background_detail_name'), table_name='professional_background_detail')
    op.drop_table('professional_background_detail')
