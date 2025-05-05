"""Эндпоинты для работы с задачами."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import task as task_crud
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.core.priority import sort_tasks_by_priority

router = APIRouter()

@router.get("/", response_model=List[Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Получить список задач пользователя."""
    tasks = await task_crud.get_tasks(db, current_user, skip=skip, limit=limit)
    return sort_tasks_by_priority(tasks)

@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Создать новую задачу."""
    return await task_crud.create_task(db, task, current_user)

@router.get("/{task_id}", response_model=Task)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Получить информацию о конкретной задаче."""
    db_task = await task_crud.get_task(db, task_id, current_user)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Обновить информацию о задаче."""
    db_task = await task_crud.update_task(db, task_id, task, current_user)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Удалить задачу."""
    success = await task_crud.delete_task(db, task_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"} 