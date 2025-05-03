from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: float = Field(default=0.0, ge=0.0, le=1.0)
    status: str = Field(default="pending")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[float] = None
    status: Optional[str] = None

class TaskInDB(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Task(TaskInDB):
    pass 