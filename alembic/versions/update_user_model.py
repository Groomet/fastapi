"""update user model

Revision ID: update_user_model
Revises: update_task_model
Create Date: 2024-05-04 13:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_user_model'
down_revision = 'update_task_model'
branch_labels = None
depends_on = None

def upgrade():
    # Add full_name column to users table
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))

def downgrade():
    # Remove full_name column from users table
    op.drop_column('users', 'full_name') 