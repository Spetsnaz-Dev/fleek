from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as _AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

async_engine = create_async_engine(
    settings.DATABASE_URL, echo=True, future=True
)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=_AsyncSession, expire_on_commit=False)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
