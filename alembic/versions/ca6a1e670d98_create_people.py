"""Create People

Revision ID: ca6a1e670d98
Revises: 1aa88ce89b93
Create Date: 2025-05-16 14:39:06.346560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca6a1e670d98'
down_revision = '1aa88ce89b93'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(length=200), nullable=False),
    sa.Column('orcid', sa.String(length=50), nullable=False),
    sa.Column('comments', sa.Text(), nullable=False),
    sa.Column('full_time_equivalent', sa.DECIMAL(precision=4, scale=2), nullable=False),
    sa.Column('job_title_id', sa.Integer(), nullable=False),
    sa.Column('professional_background_id', sa.Integer(), nullable=False),
    sa.Column('ukcrc_health_category_id', sa.Integer(), nullable=False),
    sa.Column('professional_background_detail_id', sa.Integer(), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['job_title_id'], ['job_title.id'], ),
    sa.ForeignKeyConstraint(['professional_background_detail_id'], ['professional_background_detail.id'], ),
    sa.ForeignKeyConstraint(['professional_background_id'], ['professional_background.id'], ),
    sa.ForeignKeyConstraint(['ukcrc_health_category_id'], ['ukcrc_health_category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('orcid')
    )
    op.create_index(op.f('ix_person_job_title_id'), 'person', ['job_title_id'], unique=False)
    op.create_index(op.f('ix_person_professional_background_detail_id'), 'person', ['professional_background_detail_id'], unique=False)
    op.create_index(op.f('ix_person_professional_background_id'), 'person', ['professional_background_id'], unique=False)
    op.create_index(op.f('ix_person_ukcrc_health_category_id'), 'person', ['ukcrc_health_category_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_person_ukcrc_health_category_id'), table_name='person')
    op.drop_index(op.f('ix_person_professional_background_id'), table_name='person')
    op.drop_index(op.f('ix_person_professional_background_detail_id'), table_name='person')
    op.drop_index(op.f('ix_person_job_title_id'), table_name='person')
    op.drop_table('person')
