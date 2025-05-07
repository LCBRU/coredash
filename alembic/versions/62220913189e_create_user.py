"""Create User

Revision ID: 62220913189e
Revises: a36eb9c67fb6
Create Date: 2025-05-07 15:00:21.749261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62220913189e'
down_revision = 'a36eb9c67fb6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=50), nullable=True),
    sa.Column('current_login_ip', sa.String(length=50), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('ldap_user', sa.Boolean(), nullable=True),
    sa.Column('fs_uniquifier', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier'),
    sa.UniqueConstraint('username')
    )


def downgrade() -> None:
    op.drop_table('user')
