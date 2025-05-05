"""Схемы для пользователей."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """Базовая схема пользователя."""
    email: EmailStr = Field(..., example="user@example.com")
    full_name: str = Field(..., example="Иван Иванов")
    priority: int = Field(3, ge=1, le=5, example=3)

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
    """Схема токена доступа."""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """Схема полезной нагрузки токена."""
    sub: int 