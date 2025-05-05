"""Эндпоинты для работы с категориями задач."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import category as category_crud
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter()

@router.get(
    "/",
    response_model=List[Category],
    summary="Получить категории",
    description="Возвращает список категорий пользователя."
)
async def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Получить список категорий пользователя."""
    return await category_crud.get_categories(db, current_user, skip=skip, limit=limit)

@router.post(
    "/",
    response_model=Category,
    summary="Создать категорию",
    description="Создаёт новую категорию для пользователя."
)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Создать новую категорию."""
    return await category_crud.create_category(db, category, current_user)

@router.get(
    "/{category_id}",
    response_model=Category,
    summary="Получить категорию",
    description="Получить информацию о конкретной категории по её идентификатору."
)
async def read_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Получить информацию о конкретной категории."""
    db_category = await category_crud.get_category(db, category_id, current_user)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put(
    "/{category_id}",
    response_model=Category,
    summary="Обновить категорию",
    description="Обновить информацию о категории по её идентификатору."
)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Обновить информацию о категории."""
    db_category = await category_crud.update_category(db, category_id, category, current_user)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete(
    "/{category_id}",
    summary="Удалить категорию",
    description="Удалить категорию по её идентификатору."
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """Удалить категорию."""
    success = await category_crud.delete_category(db, category_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"} 