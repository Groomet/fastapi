from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5, description="Priority from 1 to 5")
    status: str = Field(default="pending")
    due_date: Optional[date] = None
    estimated_duration: Optional[float] = Field(default=0, ge=0)
    category_id: Optional[int] = None

    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ["pending", "in_progress", "blocked", "completed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
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