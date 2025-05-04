from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск приложения
    await init_db()
    yield
    # Остановка приложения
    # Добавьте сюда код для завершения работы, если нужно

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Task Management API with Priority Algorithm",
    version="1.0.0",
    lifespan=lifespan,
)

# Настройка CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение основного роутера API
app.include_router(api_router, prefix=settings.API_V1_STR)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
    
