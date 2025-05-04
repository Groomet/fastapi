"""update task model

Revision ID: update_task_model
Revises: 
Create Date: 2024-03-21 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_task_model'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Изменяем тип поля priority с Float на Integer
    op.alter_column('tasks', 'priority',
               existing_type=sa.Float(),
               type_=sa.Integer(),
               existing_nullable=True,
               existing_server_default=sa.text('0.0'))
    
    # Добавляем новые поля
    op.add_column('tasks', sa.Column('due_date', sa.Date(), nullable=True))
    op.add_column('tasks', sa.Column('estimated_duration', sa.Float(), nullable=True))

def downgrade():
    # Возвращаем тип поля priority обратно к Float
    op.alter_column('tasks', 'priority',
               existing_type=sa.Integer(),
               type_=sa.Float(),
               existing_nullable=True,
               existing_server_default=sa.text('0.0'))
    
    # Удаляем добавленные поля
    op.drop_column('tasks', 'estimated_duration')
    op.drop_column('tasks', 'due_date') 