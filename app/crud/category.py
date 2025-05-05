"""CRUD операции для категорий задач."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

async def get_categories(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Category]:
    """Получить список категорий пользователя."""
    query = select(Category).where(Category.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_category(
    db: AsyncSession,
    category_id: int,
    user_id: int
) -> Optional[Category]:
    """Получить категорию по ID."""
    query = select(Category).where(
        Category.id == category_id,
        Category.user_id == user_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_category(
    db: AsyncSession,
    category: CategoryCreate,
    user_id: int
) -> Category:
    """Создать новую категорию."""
    db_category = Category(**category.model_dump(), user_id=user_id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def update_category(
    db: AsyncSession,
    category_id: int,
    category: CategoryUpdate,
    user_id: int
) -> Optional[Category]:
    """Обновить категорию."""
    db_category = await get_category(db, category_id, user_id)
    if db_category:
        for key, value in category.model_dump(exclude_unset=True).items():
            setattr(db_category, key, value)
        await db.commit()
        await db.refresh(db_category)
    return db_category

async def delete_category(
    db: AsyncSession,
    category_id: int,
    user_id: int
) -> bool:
    """Удалить категорию."""
    db_category = await get_category(db, category_id, user_id)
    if db_category:
        await db.delete(db_category)
        await db.commit()
        return True
    return False 