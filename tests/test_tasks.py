"""Тесты для задач."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from httpx import AsyncClient

from main import app
from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskStatus

client = TestClient(app)

@pytest.fixture
async def test_user(db: AsyncSession):
    user = User(
        email="test@example.com",
        hashed_password="hashed_password"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@pytest.fixture
def test_token(test_user: User):
    return create_access_token(data={"sub": test_user.id})

pytestmark = pytest.mark.asyncio

async def test_create_task(client: AsyncClient, db: AsyncSession, test_user, token_headers):
    """Тест создания задачи."""
    response = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": TaskStatus.PENDING,
            "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "estimated_duration": 60,
            "category_id": None
        },
        headers=token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == TaskStatus.PENDING
    assert "id" in data

async def test_get_tasks(client: AsyncClient, db: AsyncSession, test_user, token_headers):
    """Тест получения списка задач."""
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=1,
        user_id=test_user.id
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    response = await client.get(
        "/api/v1/tasks/",
        headers=token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "Test Task"

async def test_get_task_not_found(client: AsyncClient, db: AsyncSession, token_headers):
    """Тест получения несуществующей задачи."""
    response = await client.get(
        "/api/v1/tasks/999",
        headers=token_headers
    )
    assert response.status_code == 404

async def test_update_task(client: AsyncClient, db: AsyncSession, test_user, token_headers):
    """Тест обновления задачи."""
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=1,
        user_id=test_user.id
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    response = await client.put(
        f"/api/v1/tasks/{task.id}",
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "status": TaskStatus.IN_PROGRESS
        },
        headers=token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["status"] == TaskStatus.IN_PROGRESS

async def test_delete_task(client: AsyncClient, db: AsyncSession, test_user, token_headers):
    """Тест удаления задачи."""
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=1,
        user_id=test_user.id
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    response = await client.delete(
        f"/api/v1/tasks/{task.id}",
        headers=token_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully" 