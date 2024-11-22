from sqlalchemy import String, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Промежуточная таблица user_group
class UserGroupsOrm(Base):
    __tablename__ = "user_group"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.group_id'), primary_key=True)

# Промежуточная таблица group_admins
class GroupAdminsOrm(Base):
    __tablename__ = "group_admins"

    group_id: Mapped[int] = mapped_column(ForeignKey('groups.group_id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)

# Таблица пользователей
class UsersOrm(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(256))

    # Связь с группами через таблицу user_group
    groups: Mapped[list["GroupsOrm"]] = relationship(
        "GroupsOrm",
        secondary="user_group",
        back_populates="users"
    )

    # Связь с группами через таблицу group_admins (как администратор)
    admin_groups: Mapped[list["GroupsOrm"]] = relationship(
        "GroupsOrm",
        secondary="group_admins",
        back_populates="admins"
    )

# Таблица групп
class GroupsOrm(Base):
    __tablename__ = 'groups'

    group_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(256), nullable=False)

    # Связь с пользователями через таблицу user_group
    users: Mapped[list["UsersOrm"]] = relationship(
        "UsersOrm",
        secondary="user_group",
        back_populates="groups"
    )

    # Связь с администраторами через таблицу group_admins
    admins: Mapped[list["UsersOrm"]] = relationship(
        "UsersOrm",
        secondary="group_admins",
        back_populates="admin_groups"
    )

if await Database.checkUser(user_id):
        await message.answer("ты в базе)))")
    else:
        await message.answer("ты не базе(")
        await Database.insertUser(user_id, user_name)
    
    if await Database.checkUser(user_id):
        await message.answer("ты в базе)))")
    else:
        await message.answer("ты не базе(")

    await Database.insertGroup(group_id=123445, group_name="ne_abobus")
    await Database.insertGroup(group_id=112233445566, group_name="abobus")
    await Database.insertUserGroup(user_id=user_id, group_id=112233445566)
    await Database.insertUserGroup(user_id=user_id, group_id=123445)

    if await Database.checkUserGroup(user_id, 123445):
        await message.answer("ты есть в этой группе")
    else:
        await message.answer("тебя нет в этой группе")
    
    if await Database.checkUserGroup(user_id, 112233445566):
        await message.answer("ты есть в этой группе")
    else:
        await message.answer("тебя нет в этой группе")

    await message.answer(str(await Database.selectUserGroup(user_id)))