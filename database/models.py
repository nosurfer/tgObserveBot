from typing import Annotated
from sqlalchemy import Table, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class UserGroupsOrm(Base):
    __tablename__ = "user_group"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.group_id', ondelete="CASCADE"), primary_key=True)


class GroupAdminsOrm(Base):
    __tablename__ = "group_admins"

    group_id: Mapped[int] = mapped_column(ForeignKey('groups.group_id', ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True)


class UsersOrm(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(256), nullable=False)

    groups: Mapped[list["GroupsOrm"]] = relationship(
        "GroupsOrm",
        secondary="user_group",
        back_populates="users"
    )

    admin_groups: Mapped[list["GroupsOrm"]] = relationship(
        "GroupsOrm",
        secondary="group_admins",
        back_populates="users"
    )


class GroupsOrm(Base):
    __tablename__ = 'groups'

    group_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    group_name: Mapped[str] = mapped_column(String(256), nullable=False)

    users: Mapped[list["UsersOrm"]] = relationship(
        "UsersOrm",
        secondary="user_group",
        back_populates="groups"
    )

    admins: Mapped[list["UsersOrm"]] = relationship(
        "UsersOrm",
        secondary="group_admins",
        back_populates="groups"
    )