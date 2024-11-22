import asyncio

from sqlalchemy_utils import database_exists
from sqlalchemy import select

from database.models import UsersOrm, GroupsOrm, UserGroupsOrm, GroupAdminsOrm
from database.database import async_engine, async_session_factory, Base

from database.config import settings

# https://youtu.be/vh19Mlot0NY?feature=shared


class Database:    
    @staticmethod
    async def createTables():
        if not database_exists(settings.DATABASE_URL_aiosqlite):
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insertUser(user_id: int, user_name: str) -> None:
        async with async_session_factory() as session:
            user = UsersOrm(user_id=user_id, user_name=user_name)
            session.add(user)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def insertGroup(group_id: int, group_name: str):
        async with async_session_factory() as session:
            group = GroupsOrm(group_id=user_id, group_name=user_name)
            session.add(group)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def insertUserGroup(user_id: int, group_id: str):
        async with async_session_factory() as session:
            user_group = UserGroupsOrm(user_id=user_id, group_id=group_id)
            session.add(user_group)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def selectUser(user_id: int = None):
        async with async_session_factory() as session:
            if user_id == None:
                query = select(UsersOrm)
            else:
                query = select(UsersOrm(user_id=users_id))
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def selectAdmin(group_id: int = None):
        async with async_session_factory() as session:
            if group_id == None:
                query = select(GroupsOrm)
            else:
                query = select(GroupsOrm(group_id=group_id))
            result = await session.execute(query)
            return result.scalars().all()
    
    @staticmethod
    async def checkUser(user_id: int) -> bool:
        async with async_session_factory() as session:
            query = select(UsersOrm).filter(UsersOrm.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().first() is not None
    
    @staticmethod
    async def checkGroup(group_id: int) -> bool:
        async with async_session_factory() as session:
            group = select(GroupsOrm(group_id=group_id))
            result = await session.execute(query)
            return result.scalars().first() is not None

    @staticmethod
    async def checkUserGroup(user_id: int, group_id: int) -> bool:
        async with async_session_factory() as session:
            user = await session.get(UsersOrm, user_id)
            return group_id in user.groups
    
    @staticmethod
    async def selectUserGroup(user_id: int, group_id: int) -> bool:
        async with async_session_factory() as session:
            user = await session.get(UsersOrm, user_id)
            return user.groups
    