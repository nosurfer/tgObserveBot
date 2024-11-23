import asyncio

from sqlalchemy_utils import database_exists
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from database.models import UsersOrm, GroupsOrm, UserGroupsOrm, GroupAdminsOrm
from database.database import async_engine, async_session_factory, Base

from database.config import settings

# https://youtu.be/vh19Mlot0NY?feature=shared


class Database:    
    @staticmethod
    async def createTables() -> None:
        """Create tables from models.py"""
        if not database_exists(settings.DATABASE_URL_aiosqlite):
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insertUser(user_id: int, user_name: str) -> None:
        """Insert user_id and user_name in users table"""
        async with async_session_factory() as session:
            user = UsersOrm(user_id=user_id, user_name=user_name)
            session.add(user)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def insertGroup(group_id: int, group_name: str) -> None:
        """Insert group_id and group_name in groups table"""
        async with async_session_factory() as session:
            group = GroupsOrm(group_id=group_id, group_name=group_name)
            session.add(group)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def insertUserGroup(user_id: int, group_id: str) -> None:
        """Insert user_id and group_id in user_group table"""
        async with async_session_factory() as session:
            user_group = UserGroupsOrm(user_id=user_id, group_id=group_id)
            session.add(user_group)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def insertGroupAdmin(group_id: int, user_id: str) -> None:
        """Insert group_id and user_id in group_admin table"""
        async with async_session_factory() as session:
            group_admin = GroupAdminsOrm(group_id=group_id, user_id=user_id)
            session.add(group_admin)
            await session.flush()
            await session.commit()
    
    @staticmethod
    async def selectUser(user_id: int = None) -> dict:
        """Select user by user_id or select all users with none value
        Return dict - {user_id: user_name, ...}"""
        async with async_session_factory() as session:
            if user_id is None:
                query = select(UsersOrm)
            else:
                query = select(UsersOrm).where(UsersOrm.user_id == user_id)
            result = await session.execute(query)
            users = result.scalars().all()
            return {user.user_id:user.user_name for user in users}
    
    @staticmethod
    async def selectGroup(group_id: int = None):
        """Select group by group_id or select all groups with none value
        Return dict - {group_id: group_name, ...}"""
        async with async_session_factory() as session:
            if group_id is None:
                query = select(GroupsOrm)
            else:
                query = select(GroupsOrm).where(GroupsOrm.group_id == group_id)
            result = await session.execute(query)
            groups = result.scalars().all()
            return {group.group_id:group.group_name for group in groups}

    @staticmethod
    async def selectUserGroup(user_id: int) -> dict:
        """Select group where user is admin by group_id
        Return dict - {group_id: group_name, ...}"""
        async with async_session_factory() as session:
            user = await session.get(
                UsersOrm, 
                user_id, 
                options=[selectinload(UsersOrm.groups)]
            )
            return {group.group_id:group.group_name for group in user.groups}
    
    @staticmethod
    async def selectAdmin(user_id: int = None, group_id: int = None) -> dict:
        """Select group_id and user_id where user is Admin by user_id or group_id or all values with None
        Return dict {group_id: user_id, ...}"""
        async with async_session_factory() as session:
            if user_id is None and group_id is None:
                query = select(GroupAdminsOrm)
            elif user_id is not None:
                query = select(GroupAdminsOrm).where(GroupAdminsOrm.user_id == user_id)
            else:
                query = select(GroupAdminsOrm).where(GroupAdminsOrm.group_id == group_id)
            result = await session.execute(query)
            groups = result.scalars().all()
            return {group.group_id:group.user_id for group in groups}
    
    @staticmethod
    async def checkUser(user_id: int) -> bool:
        """Check user in users table"""
        async with async_session_factory() as session:
            query = select(UsersOrm).where(UsersOrm.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().first() is not None
    
    @staticmethod
    async def checkGroup(group_id: int) -> bool:
        """Check group in groups table"""
        async with async_session_factory() as session:
            query = select(GroupsOrm).where(GroupsOrm.group_id == group_id)
            result = await session.execute(query)
            return result.scalars().first() is not None

    @staticmethod
    async def checkUserGroup(user_id: int, group_id: int) -> bool:
        """Verify that the user belongs to a group"""
        async with async_session_factory() as session:
            user = await session.get(
                UsersOrm, 
                user_id, 
                options=[selectinload(UsersOrm.groups)]
            )
            return any(group.group_id == group_id for group in user.groups)