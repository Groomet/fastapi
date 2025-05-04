from typing import List
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
    query = select(Category).where(Category.user_id == user_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_category(
    db: AsyncSession,
    category_id: int,
    user_id: int
) -> Category:
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
) -> Category:
    db_category = await get_category(db, category_id, user_id)
    if not db_category:
        return None
    
    for field, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)
    
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def delete_category(
    db: AsyncSession,
    category_id: int,
    user_id: int
) -> bool:
    db_category = await get_category(db, category_id, user_id)
    if not db_category:
        return False
    
    await db.delete(db_category)
    await db.commit()
    return True 