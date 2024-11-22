from typing import Annotated
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base

# Аннотации для упрощения записи типов
intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, 256]

class UsersOrm(Base):
    __tablename__ = "users"

    user_id: Mapped[intpk]
    user_name: Mapped[str_256]

    # Связь с таблицей групп через таблицу связи UserGroupsOrm
    groups: Mapped["GroupsOrm"] = relationship(secondary="user_groups", back_populates="users")


class GroupsOrm(Base):
    __tablename__ = "groups"

    group_id: Mapped[intpk]
    group_name: Mapped[str_256]

    # Связь с таблицей пользователей через таблицу связи UserGroupsOrm
    users: Mapped["UsersOrm"] = relationship(secondary="user_groups", back_populates="groups")
    
    # Связь с таблицей администраторов группы
    admins: Mapped["GroupAdminsOrm"] = relationship(back_populates="group")


class UserGroupsOrm(Base):
    __tablename__ = "user_groups"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id", ondelete="CASCADE"))

    # В таблице связи UserGroupsOrm не нужно устанавливать back_populates
    # Все связи уже установлены в UsersOrm и GroupsOrm, поэтому можно удалить
    # user: Mapped["UsersOrm"] = relationship(back_populates="groups")
    # group: Mapped["GroupsOrm"] = relationship(back_populates="users")


class GroupAdminsOrm(Base):
    __tablename__ = "group_admins"

    id: Mapped[intpk]
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))

    # Обратная связь с таблицами пользователей и групп
    group: Mapped["GroupsOrm"] = relationship(back_populates="admins")
    user: Mapped["UsersOrm"] = relationship()