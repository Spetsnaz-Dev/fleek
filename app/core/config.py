# import os
from pydantic_settings import BaseSettings
# import dotenv
# dotenv.load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://ravindra:password@db:5432/fleek"
    REDIS_URL: str = "redis://redis:6379/0"
    STORAGE_BACKEND: str = "local"
    LOCAL_MEDIA_PATH: str = "media"
    REPLICATE_API_TOKEN: str = "mock-token"

    class Config:
        env_file = ".env"

settings = Settings()
