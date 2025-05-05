"""Схемы для категорий задач."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    """Базовая схема категории."""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Схема для создания категории."""
    pass

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