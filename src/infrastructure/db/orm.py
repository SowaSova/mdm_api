from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from src.core.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
