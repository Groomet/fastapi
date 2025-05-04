from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_current_user
from app.core.config import settings
from app.crud import user as user_crud
from app.schemas.user import User, UserCreate, Token, UserUpdate

router = APIRouter()

@router.post("/register", response_model=User)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    db_user = await user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Почта уже зарегистрирована")
    return await user_crud.create_user(db, user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверная почта или пароль")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_current_user(
    current_user: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user(db, current_user)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.update_user(db, current_user, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user(db, current_user)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")
    
    await user_crud.update_user_password(db, current_user, new_password)
    return {"message": "Пароль успешно обновлен"} 