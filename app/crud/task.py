from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.priority import calculate_priority

async def get_task(db: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def get_tasks(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_task(db: AsyncSession, task: TaskCreate, user_id: int) -> Task:
    db_task = Task(
        **task.model_dump(),
        user_id=user_id
    )
    db_task.priority = calculate_priority(db_task)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(
    db: AsyncSession,
    task_id: int,
    task: TaskUpdate,
    user_id: int
) -> Optional[Task]:
    db_task = await get_task(db, task_id, user_id)
    if not db_task:
        return None
    
    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db_task.priority = calculate_priority(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> bool:
    result = await db.execute(
        delete(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    await db.commit()
    return result.rowcount > 0 