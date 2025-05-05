"""Схемы для категорий задач."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    """Базовая схема категории."""
    name: str = Field(..., example="Учёба")
    description: Optional[str] = Field(None, example="Задачи, связанные с учёбой")

class CategoryCreate(CategoryBase):
    """Схема для создания категории."""
    # pass

class CategoryUpdate(CategoryBase):
    """Схема для обновления категории."""
    name: Optional[str] = None

class Category(CategoryBase):
    """Схема категории."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Конфигурация схемы."""
        from_attributes = True 