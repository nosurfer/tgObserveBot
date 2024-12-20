import asyncio

from sqlalchemy_utils import database_exists
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete, update, and_, text

from database.models import UsersOrm, GroupsOrm, UserGroupsOrm
from database.database import async_engine, async_session_factory, Base

from database.config import settings

# https://youtu.be/vh19Mlot0NY?feature=shared

# createTables - создаёт базу данных
# insertUser - добавляет пользователя в базу
# insertGroup - добавляет группу в базу
# insertUserGroup - добавляет айди пользователя и группы с учётом прав админа
# selectUser - достаёт айди пользователя и имя пользователя
# selectGroup - достаёт айди группы и имя группы
# selectUserGroup - достаёт группы пользователя, или пользователей группы с их правами
# selectAdmin - возвращает группы где пользователь админ, или пользователей по группе, или всех админов
# checkUser - проверяет пользователя в базе данных
# checkGroup - проверяет группу в базе данных
# checkUserGroup - проверяет привязана ли группа к пользователю
# checkAdmin - проверяет, является ли польвотелем админом в группе
# updateAdmin - обновляет права пользователя для группы
# deleteGroup - удаляет группу из базы данных вместе со всеми данными привязанными к ней

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
            group_name = group_name.replace("*", "")
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
    async def selectUser(user_id: int = None) -> list:
        """Select user by user_id or select all users with none value
        Return list - [(user_id, user_name) ...]"""
        async with async_session_factory() as session:
            if user_id is None:
                query = select(UsersOrm)
            else:
                query = select(UsersOrm).where(UsersOrm.user_id == user_id)
            result = await session.execute(query)
            users = result.scalars().all()
            return [(user.user_id, user.user_name) for user in users]
    
    @staticmethod
    async def selectGroup(group_id: int = None) -> list:
        """Select group by group_id or select all groups with none value
        Return list - [(group_id, group_name) ...]"""
        async with async_session_factory() as session:
            if group_id is None:
                query = select(GroupsOrm)
            else:
                query = select(GroupsOrm).where(GroupsOrm.group_id == group_id)
            result = await session.execute(query)
            groups = result.scalars().all()
            return [(group.group_id, group.group_name) for group in groups]

    @staticmethod
    async def selectUserGroup(user_id: int = None, group_id: int = None) -> list:
        """Select group where be user by group_id or select user where user in
        Return list - [(group_id, user_id, is_admin) ...]"""
        async with async_session_factory() as session:
            if user_id is None:
                query = select(UserGroupsOrm).where(UserGroupsOrm.user_id == user_id)
            elif group_id is None:
                query = select(UserGroupsOrm).where(UserGroupsOrm.group_id == group_id)
            else:
                raise MyCrustomError("Parameter doesnt exist")
            result = await session.execute(query)
            return [(value.group_id, value.user_id, value.is_admin) for value in result]
    
    @staticmethod
    async def selectAdmin(user_id: int = None, group_id: int = None) -> list:
        """Select user_id by group_id or group_id by user_id, if parameters doesnt exist -> group_id and user_id
        Return list - [user_id, ...] or [group_id, ...] or [(group_id, user_id), ...]"""
        async with async_session_factory() as session:
            if user_id is not None:
                query = select(UserGroupsOrm).where(_and(UserGroupsOrm.user_id == user_id, UserGroupsOrm.is_admin == 1))
                result = await session.execute(query)
                return [value.group_id for value in result]
            elif group_id is not None:
                query = select(UserGroupsOrm).where(_and(UserGroupsOrm.group_id == group_id, UserGroupsOrm.is_admin == 1))
                result = await session.execute(query)
                return [value.user_id for value in result]
            else:
                query = select(UserGroupsOrm).where(UserGroupsOrm.is_admin == 1)
                result = await session.execute(query)
                return [(value.group_id, value.user_id) for value in result]
        
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
    async def checkAdmin(user_id: int, group_id: int) -> bool:
        """Check admin status of user in group"""
        async with async_session_factory() as session:
            query = select(UserGroupsOrm).where(
                and_(
                    UserGroupsOrm.group_id == group_id, 
                    UserGroupsOrm.user_id == user_id,
                    UserGroupsOrm.is_admin == 1
                )
            )
            result = await session.execute(query)
            return result.scalars().first() is not None

    @staticmethod
    async def checkUserGroup(user_id: int, group_id: int) -> bool:
        """Verify that the user belongs to a group"""
        async with async_session_factory() as session:
            query = select(UserGroupsOrm).where(
                and_(
                    UserGroupsOrm.group_id == group_id,
                    UserGroupsOrm.user_id == user_id
                )
            )
            result = await session.execute(query)
            return result.scalars().first() is not None

    @staticmethod
    async def updateAdmin(user_id: int, group_id: int, value: bool) -> None:
        """Updates user privileges by user_id and group_id in user_groups"""
        async with async_session_factory() as session:
            await session.execute(update(UserGroupsOrm).where(
                and_(
                    UserGroupsOrm.user_id == user_id,
                    UserGroupsOrm.group_id == group_id
                )).values({"is_admin": int(value)})
            )
            await session.flush()
            await session.commit()


    @staticmethod
    async def getCurGroup(user_id: int) -> int:
        """Get group id by user_id or None"""
        async with async_session_factory() as session:
            query = select(UserGroupsOrm).where(and_(UserGroupsOrm.user_id == user_id, UserGroupsOrm.select_group == 1))
            result = await session.execute(query)
            if result.scalars().first() is not None:
                return [value.group_id for value in result][0]
            return None


    @staticmethod
    async def setCurGroup(user_id: int, group_id: int) -> None:
        """Set group for admin"""
        async with async_session_factory() as session:
            await session.execute(
                update(UserGroupsOrm).where(and_(
                    UserGroupsOrm.user_id == user_id,
                    UserGroupsOrm.select_group == 1
                )).values({"select_group": 0}))
            await session.execute(
                update(UserGroupsOrm).where(and_(
                        UserGroupsOrm.user_id == user_id,
                        UserGroupsOrm.group_id == group_id
                    )).values({"select_group": 1}))
            await session.flush()
            await session.commit()


    @staticmethod
    async def deleteGroup(group_id: int) -> None:
        """Delete group_id and group_name in every table"""
        async with async_session_factory() as session:
            await session.execute(text("PRAGMA foreign_keys = ON"))
            query = delete(GroupsOrm).where(GroupsOrm.group_id == group_id)
            await session.execute(query)
            await session.commit()