"""Схемы для задач."""

from enum import Enum
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class TaskStatus(str, Enum):
    """Статусы задачи."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"

class TaskBase(BaseModel):
    """Базовая схема задачи."""
    title: str = Field(..., example="Сделать домашку")
    description: Optional[str] = Field(None, example="Выполнить задание по математике")
    priority: int = Field(ge=1, le=5, description="Priority from 1 to 5", example=3)
    status: TaskStatus = Field(default=TaskStatus.PENDING, example="pending")
    due_date: Optional[date] = Field(None, example="2024-07-01")
    estimated_duration: Optional[float] = Field(default=0, ge=0, example=60)
    category_id: Optional[int] = Field(None, example=1)

    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ["pending", "in_progress", "blocked", "completed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v

class TaskCreate(TaskBase):
    """Схема для создания задачи."""
    # pass

class TaskUpdate(TaskBase):
    """Схема для обновления задачи."""
    title: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    estimated_duration: Optional[float] = Field(None, ge=0)

    @validator('status')
    def validate_status(cls, v):
        if v is None:
            return v
        allowed_statuses = ["pending", "in_progress", "blocked", "completed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v

class TaskInDB(TaskBase):
    """Схема задачи в БД."""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        """Конфигурация схемы."""
        from_attributes = True

class Task(TaskInDB):
    """Схема задачи для API."""
    # pass

class ScheduledTask(TaskInDB):
    """Схема запланированной задачи."""
    start_time: datetime
    end_time: datetime

class ScheduleResponse(BaseModel):
    """Схема ответа для расписания задач."""
    tasks: List[ScheduledTask]
    total_duration: float
    utilization_rate: float 