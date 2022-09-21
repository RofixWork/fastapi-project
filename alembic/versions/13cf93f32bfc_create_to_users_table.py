"""create to users table

Revision ID: 13cf93f32bfc
Revises: 
Create Date: 2022-09-20 16:40:19.615056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13cf93f32bfc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer, primary_key=True), 
        sa.Column('username', sa.String(length=30), nullable=False, unique=True),
        sa.Column('email', sa.String(length=150), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table('users')
