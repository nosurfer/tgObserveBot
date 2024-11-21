from typing import Annotated

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, 256]

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    user_id: Mapped[int]
    user_name: Mapped[str_256]


class GroupsOrm(Base):
    __tablename__ = "groups"

    id: Mapped[intpk]
    group_id: Mapped[int]
    group_name: Mapped[str_256]


class UserGroupsOrm(Base):
    __tablename__ = "user_groups"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id", ondelete="CASCADE"))


class GroupAdminsOrm(Base):
    __tablename__ = "group_admins"

    id: Mapped[intpk]
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id", ondelete="CASCADE"))
