from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    # Настройки API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task Management API"
    
    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Настройки CORS
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    
    # Настройки безопасности
    SECRET_KEY: str = "your-secret-key-here"  # Измените это значение в production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Настройки базы данных
    DATABASE_URL: str = "sqlite+aiosqlite:///./task_management.db"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 