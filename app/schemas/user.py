"""Схемы для пользователей."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """Базовая схема пользователя."""
    email: EmailStr
    full_name: str
    priority: int = 3  # Приоритет пользователя от 1 до 5

class UserCreate(UserBase):
    """Схема для создания пользователя."""
    password: str

class UserUpdate(UserBase):
    """Схема для обновления пользователя."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    priority: Optional[int] = None

class User(UserBase):
    """Схема пользователя."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Конфигурация схемы."""
        from_attributes = True

class UserInDB(User):
    """Схема пользователя в БД."""
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: int 