"""Create Project

Revision ID: cfefa58ad527
Revises: 62220913189e
Create Date: 2025-05-07 15:01:07.037286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfefa58ad527'
down_revision = '62220913189e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('comments', sa.Text(), nullable=False),
    sa.Column('local_rec_number', sa.String(length=50), nullable=True),
    sa.Column('iras_number', sa.String(length=50), nullable=True),
    sa.Column('cpms_id', sa.String(length=50), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('participants_recruited_to_centre_fy', sa.Integer(), nullable=False),
    sa.Column('brc_funding', sa.Integer(), nullable=False),
    sa.Column('main_funding_brc_funding', sa.Integer(), nullable=True),
    sa.Column('total_external_funding_award', sa.Integer(), nullable=False),
    sa.Column('sensitive', sa.Boolean(), nullable=False),
    sa.Column('first_in_human', sa.Boolean(), nullable=False),
    sa.Column('link_to_nihr_transactional_research_collaboration', sa.Boolean(), nullable=False),
    sa.Column('crn_rdn_portfolio_study', sa.Boolean(), nullable=False),
    sa.Column('rec_approval_required', sa.Boolean(), nullable=False),
    sa.Column('randomised_trial', sa.Boolean(), nullable=False),
    sa.Column('project_status_id', sa.Integer(), nullable=False),
    sa.Column('theme_id', sa.Integer(), nullable=False),
    sa.Column('ukcrc_health_category_id', sa.Integer(), nullable=False),
    sa.Column('nihr_priority_area_id', sa.Integer(), nullable=False),
    sa.Column('ukcrc_research_activity_code_id', sa.Integer(), nullable=False),
    sa.Column('racs_sub_category_id', sa.Integer(), nullable=True),
    sa.Column('research_type_id', sa.Integer(), nullable=False),
    sa.Column('methodology_id', sa.Integer(), nullable=False),
    sa.Column('expected_impact_id', sa.Integer(), nullable=False),
    sa.Column('trial_phase_id', sa.Integer(), nullable=True),
    sa.Column('main_funding_source_id', sa.Integer(), nullable=False),
    sa.Column('main_funding_category_id', sa.Integer(), nullable=False),
    sa.Column('main_funding_dhsc_nihr_funding_id', sa.Integer(), nullable=True),
    sa.Column('main_funding_industry_id', sa.Integer(), nullable=True),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['expected_impact_id'], ['expected_impact.id'], ),
    sa.ForeignKeyConstraint(['main_funding_category_id'], ['main_funding_category.id'], ),
    sa.ForeignKeyConstraint(['main_funding_dhsc_nihr_funding_id'], ['main_funding_dhsc_nihr_funding.id'], ),
    sa.ForeignKeyConstraint(['main_funding_industry_id'], ['main_funding_industry.id'], ),
    sa.ForeignKeyConstraint(['main_funding_source_id'], ['main_funding_source.id'], ),
    sa.ForeignKeyConstraint(['methodology_id'], ['methodology.id'], ),
    sa.ForeignKeyConstraint(['nihr_priority_area_id'], ['nihr_priority_area.id'], ),
    sa.ForeignKeyConstraint(['project_status_id'], ['project_status.id'], ),
    sa.ForeignKeyConstraint(['racs_sub_category_id'], ['racs_sub_category.id'], ),
    sa.ForeignKeyConstraint(['research_type_id'], ['research_type.id'], ),
    sa.ForeignKeyConstraint(['theme_id'], ['theme.id'], ),
    sa.ForeignKeyConstraint(['trial_phase_id'], ['trial_phase.id'], ),
    sa.ForeignKeyConstraint(['ukcrc_health_category_id'], ['ukcrc_health_category.id'], ),
    sa.ForeignKeyConstraint(['ukcrc_research_activity_code_id'], ['ukcrc_research_activity_code.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpms_id'),
    sa.UniqueConstraint('iras_number'),
    sa.UniqueConstraint('local_rec_number'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_project_end_date'), 'project', ['end_date'], unique=False)
    op.create_index(op.f('ix_project_expected_impact_id'), 'project', ['expected_impact_id'], unique=False)
    op.create_index(op.f('ix_project_main_funding_category_id'), 'project', ['main_funding_category_id'], unique=False)
    op.create_index(op.f('ix_project_main_funding_dhsc_nihr_funding_id'), 'project', ['main_funding_dhsc_nihr_funding_id'], unique=False)
    op.create_index(op.f('ix_project_main_funding_industry_id'), 'project', ['main_funding_industry_id'], unique=False)
    op.create_index(op.f('ix_project_main_funding_source_id'), 'project', ['main_funding_source_id'], unique=False)
    op.create_index(op.f('ix_project_methodology_id'), 'project', ['methodology_id'], unique=False)
    op.create_index(op.f('ix_project_nihr_priority_area_id'), 'project', ['nihr_priority_area_id'], unique=False)
    op.create_index(op.f('ix_project_project_status_id'), 'project', ['project_status_id'], unique=False)
    op.create_index(op.f('ix_project_racs_sub_category_id'), 'project', ['racs_sub_category_id'], unique=False)
    op.create_index(op.f('ix_project_research_type_id'), 'project', ['research_type_id'], unique=False)
    op.create_index(op.f('ix_project_start_date'), 'project', ['start_date'], unique=False)
    op.create_index(op.f('ix_project_theme_id'), 'project', ['theme_id'], unique=False)
    op.create_index(op.f('ix_project_trial_phase_id'), 'project', ['trial_phase_id'], unique=False)
    op.create_index(op.f('ix_project_ukcrc_health_category_id'), 'project', ['ukcrc_health_category_id'], unique=False)
    op.create_index(op.f('ix_project_ukcrc_research_activity_code_id'), 'project', ['ukcrc_research_activity_code_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_project_ukcrc_research_activity_code_id'), table_name='project')
    op.drop_index(op.f('ix_project_ukcrc_health_category_id'), table_name='project')
    op.drop_index(op.f('ix_project_trial_phase_id'), table_name='project')
    op.drop_index(op.f('ix_project_theme_id'), table_name='project')
    op.drop_index(op.f('ix_project_start_date'), table_name='project')
    op.drop_index(op.f('ix_project_research_type_id'), table_name='project')
    op.drop_index(op.f('ix_project_racs_sub_category_id'), table_name='project')
    op.drop_index(op.f('ix_project_project_status_id'), table_name='project')
    op.drop_index(op.f('ix_project_nihr_priority_area_id'), table_name='project')
    op.drop_index(op.f('ix_project_methodology_id'), table_name='project')
    op.drop_index(op.f('ix_project_main_funding_source_id'), table_name='project')
    op.drop_index(op.f('ix_project_main_funding_industry_id'), table_name='project')
    op.drop_index(op.f('ix_project_main_funding_dhsc_nihr_funding_id'), table_name='project')
    op.drop_index(op.f('ix_project_main_funding_category_id'), table_name='project')
    op.drop_index(op.f('ix_project_expected_impact_id'), table_name='project')
    op.drop_index(op.f('ix_project_end_date'), table_name='project')
    op.drop_table('project')
