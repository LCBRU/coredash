"""Create Expenditure

Revision ID: 39317237f59b
Revises: a26b79b851b6
Create Date: 2025-06-02 17:45:52.493110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39317237f59b'
down_revision = 'a26b79b851b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expenditure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blood', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('cancer_and_neoplasms', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('cardiovascular', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('congenital_disorders', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('ear', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('eye', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('infection', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('inflammatory_and_immune_system', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('injuries_and_accidents', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('mental_health', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('metabolic_and_endocrine', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('musculoskeletal', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('oral_and_gastrointestinal', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('renal_and_urogenital', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('reproductive_health_and_childbirth', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('respiratory', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('skin', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('stroke', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('generic_health_relevance', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('disputed_aetiology_and_other', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('last_update_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('last_update_by', sa.String(length=200), nullable=False),
    sa.Column('created_by', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expenditure')
    # ### end Alembic commands ###
