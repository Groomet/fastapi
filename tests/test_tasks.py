import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.models.user import User
from app.models.task import Task

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

@pytest.mark.asyncio
async def test_create_task(test_token: str):
    response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": 0.5
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["priority"] == 0.5

@pytest.mark.asyncio
async def test_get_tasks(test_token: str, test_user: User, db: AsyncSession):
    # Create a test task
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=0.5,
        user_id=test_user.id
    )
    db.add(task)
    await db.commit()

    response = client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == "Test Task"

@pytest.mark.asyncio
async def test_get_task_not_found(test_token: str):
    response = client.get(
        "/api/v1/tasks/999",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_task(test_token: str, test_user: User, db: AsyncSession):
    # Create a test task
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=0.5,
        user_id=test_user.id
    )
    db.add(task)
    await db.commit()

    response = client.put(
        f"/api/v1/tasks/{task.id}",
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "priority": 0.8
        },
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["priority"] == 0.8

@pytest.mark.asyncio
async def test_delete_task(test_token: str, test_user: User, db: AsyncSession):
    # Create a test task
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=0.5,
        user_id=test_user.id
    )
    db.add(task)
    await db.commit()

    response = client.delete(
        f"/api/v1/tasks/{task.id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully" 