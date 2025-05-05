"""Тесты для аутентификации и авторизации."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)

pytestmark = pytest.mark.asyncio

async def test_register(client: TestClient, db: AsyncSession):
    """Тест регистрации пользователя."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            "priority": 3
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data

async def test_login(client: TestClient, db: AsyncSession):
    """Тест входа пользователя."""
    # Создаем тестового пользователя
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        priority=3
    )
    db.add(user)
    await db.commit()

    # Пытаемся войти
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_read_current_user(client: TestClient, db: AsyncSession, token_headers):
    """Тест получения информации о текущем пользователе."""
    response = await client.get("/api/v1/auth/me", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "full_name" in data

async def test_update_current_user(client: TestClient, db: AsyncSession, token_headers):
    """Тест обновления информации о текущем пользователе."""
    response = await client.put(
        "/api/v1/auth/me",
        headers=token_headers,
        json={
            "full_name": "Updated Name",
            "priority": 4
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["priority"] == 4

async def test_change_password(client: TestClient, db: AsyncSession, token_headers):
    """Тест смены пароля."""
    response = await client.put(
        "/api/v1/auth/change-password",
        headers=token_headers,
        json={
            "current_password": "testpassword",
            "new_password": "newpassword"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

@pytest.mark.asyncio
async def test_register_duplicate_email(test_user: User):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_wrong_password(test_user: User):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

@pytest.mark.asyncio
async def test_login_nonexistent_user():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password" 