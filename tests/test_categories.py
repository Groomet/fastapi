"""Тесты для категорий задач."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_category(client: AsyncClient, db: AsyncSession, token_headers):
    """Тест создания категории."""
    response = await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json={
            "name": "Test Category",
            "description": "Test Description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"
    assert "id" in data

async def test_read_categories(client: AsyncClient, db: AsyncSession, token_headers):
    """Тест получения списка категорий."""
    response = await client.get("/api/v1/categories/", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_read_category(client: AsyncClient, db: AsyncSession, token_headers):
    """Тест получения информации о категории."""
    create_response = await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json={
            "name": "Test Category",
            "description": "Test Description"
        }
    )
    category_id = create_response.json()["id"]
    response = await client.get(f"/api/v1/categories/{category_id}", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"

async def test_update_category(client: AsyncClient, db: AsyncSession, token_headers):
    """Тест обновления категории."""
    create_response = await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json={
            "name": "Test Category",
            "description": "Test Description"
        }
    )
    category_id = create_response.json()["id"]
    response = await client.put(
        f"/api/v1/categories/{category_id}",
        headers=token_headers,
        json={
            "name": "Updated Category",
            "description": "Updated Description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Category"
    assert data["description"] == "Updated Description"

async def test_delete_category(client: AsyncClient, db: AsyncSession, token_headers):
    """Тест удаления категории."""
    create_response = await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json={
            "name": "Test Category",
            "description": "Test Description"
        }
    )
    category_id = create_response.json()["id"]
    response = await client.delete(f"/api/v1/categories/{category_id}", headers=token_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Category deleted successfully" 