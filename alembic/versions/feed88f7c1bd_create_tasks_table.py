"""create tasks table

Revision ID: feed88f7c1bd
Revises: 13cf93f32bfc
Create Date: 2022-09-20 16:57:50.886954

"""
from alembic import op
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, text


# revision identifiers, used by Alembic.
revision = 'feed88f7c1bd'
down_revision = '13cf93f32bfc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tasks' ,Column('id', Integer, primary_key=True),
    Column('task_name', String, nullable=False, unique=True),
    Column('completed', Boolean, nullable=False, server_default='FALSE'),
     Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )


def downgrade() -> None:
    op.drop_table('tasks')
