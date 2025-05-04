from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5, default=1)
    due_date: Optional[date] = None
    estimated_duration: Optional[float] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    status: Optional[str] = None

class TaskInDB(TaskBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class Task(TaskInDB):
    pass

class ScheduledTask(TaskInDB):
    start_time: datetime
    end_time: datetime

class ScheduleResponse(BaseModel):
    tasks: List[ScheduledTask]
    total_duration: float
    utilization_rate: float 