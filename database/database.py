from sqlalchemy.ext.asyncio import create_async_engine, async_session
from sqlalchemy.orm import DeclarativeBase

from database.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_aiosqlite,
    echo=True
)

async_session = async_session(async_engine)

class Base(DeclarativeBase):
    pass