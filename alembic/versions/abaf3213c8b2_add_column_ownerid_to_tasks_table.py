"""add column ownerid to tasks table

Revision ID: abaf3213c8b2
Revises: feed88f7c1bd
Create Date: 2022-09-20 17:48:00.384548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abaf3213c8b2'
down_revision = 'feed88f7c1bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('owner_id',sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))


def downgrade() -> None:
    op.drop_column('tasks', 'owner_id')
