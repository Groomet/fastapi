from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskInDB, ScheduleResponse, ScheduledTask
from app.crud import task as task_crud
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/schedule", response_model=ScheduleResponse)
def get_task_schedule(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получить расписание задач на указанный период.
    Алгоритм планирования:
    1. Сортировка по приоритету и сроку выполнения
    2. Распределение задач по временным слотам
    3. Учет предполагаемой длительности
    """
    # Получаем все задачи пользователя
    tasks = task_crud.get_user_tasks(db, user_id=current_user.id)
    
    # Фильтруем задачи по периоду
    tasks = [task for task in tasks if task.due_date and start_date.date() <= task.due_date <= end_date.date()]
    
    # Сортируем задачи по приоритету и сроку выполнения
    tasks.sort(key=lambda x: (x.priority, x.due_date))
    
    scheduled_tasks = []
    current_time = start_date
    total_duration = 0
    
    for task in tasks:
        if not task.estimated_duration:
            continue
            
        # Создаем временной слот для задачи
        task_duration = timedelta(hours=task.estimated_duration)
        end_time = current_time + task_duration
        
        # Проверяем, не выходит ли задача за пределы периода
        if end_time > end_date:
            break
            
        scheduled_task = ScheduledTask(
            **task.__dict__,
            start_time=current_time,
            end_time=end_time
        )
        scheduled_tasks.append(scheduled_task)
        
        current_time = end_time
        total_duration += task.estimated_duration
    
    # Рассчитываем коэффициент использования времени
    total_period = (end_date - start_date).total_seconds() / 3600  # в часах
    utilization_rate = total_duration / total_period if total_period > 0 else 0
    
    return ScheduleResponse(
        tasks=scheduled_tasks,
        total_duration=total_duration,
        utilization_rate=utilization_rate
    ) 