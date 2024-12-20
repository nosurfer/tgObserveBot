from typing import Annotated
from sqlalchemy import Table, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from database.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
str256 = Annotated[str, mapped_column(String(256))]


class UserGroupsOrm(Base):
    __tablename__ = "user_group"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.group_id', ondelete="CASCADE"), primary_key=True)
    is_admin: Mapped[int] = mapped_column(server_default="0", nullable=False)
    select_group: Mapped[int] = mapped_column(nullable=True)

    user = relationship("UsersOrm", back_populates="user_groups")
    group = relationship("GroupsOrm", back_populates="user_groups")


class UsersOrm(Base):
    __tablename__ = 'users'

    user_id: Mapped[intpk]
    user_name: Mapped[str256]

    user_groups: Mapped[list["UserGroupsOrm"]] = relationship(
        "UserGroupsOrm",
        back_populates="user",
        cascade="all, delete"
    )

    groups: Mapped[list["GroupsOrm"]] = relationship(
        "GroupsOrm",
        secondary="user_group",
        back_populates="users",
        cascade="all, delete"
    )


class GroupsOrm(Base):
    __tablename__ = 'groups'

    group_id: Mapped[intpk]
    group_name: Mapped[str256]

    user_groups: Mapped[list["UserGroupsOrm"]] = relationship(
        "UserGroupsOrm",
        back_populates="group",
        cascade="all, delete"
    )

    users: Mapped[list["UsersOrm"]] = relationship(
        "UsersOrm",
        secondary="user_group",  
        back_populates="groups",
        cascade="all, delete"
    )