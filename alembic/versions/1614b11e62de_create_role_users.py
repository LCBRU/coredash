"""Create Role Users

Revision ID: 1614b11e62de
Revises: cfefa58ad527
Create Date: 2025-05-07 15:02:09.251396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1614b11e62de'
down_revision = 'cfefa58ad527'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )


def downgrade() -> None:
    op.drop_table('roles_users')
