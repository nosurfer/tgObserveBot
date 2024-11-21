import asyncio

from sqlalchemy_utils import database_exists
from sqlalchemy import insert

from database.models import UsersOrm
from database.database import async_engine, async_session, Base

from database.config import settings

# https://youtu.be/vh19Mlot0NY?feature=shared

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            if not database_exists(settings.DATABASE_URL_aiosqlite):
                asyncio.run(create_tables())
            cls._instance._engine = async_engine
            cls._instance._session = async_session
        return cls._instance
    

    async def insertUser(self, user_id, user_name):
        statement = UsersOrm(user_id=user_id, user_name=user_name)
        async with self._instance._session() as session:
            session.add(statement)
            await session.commit()
