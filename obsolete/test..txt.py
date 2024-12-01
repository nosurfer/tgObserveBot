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


    if await Database.checkUser(user_id):
        msg += f"{mention}, вы уже прошли регистрацию.\n\n***Dev by @Sirius_Real, @ownnickname***"
        await message.answer(msg, parse_mode="Markdown")
    else:
        user_fullname = ("@" + message.from_user.username) or (message.from_user.first_name or "" + " " + message.from_user.last_name or "")
        await Database.insertUser(user_id, user_fullname)
        msg += f"{mention}, вы были успешно зарегистрированы!\n\n***Dev by @Sirius_Real, @ownnickname***"
        await message.answer(msg, parse_mode="Markdown")



# @router.message(F.poll)
# async def read_poll_handler(message: Message):
#     global polls
#     polls.append(message.poll.poll_id)
#     msg = message.poll
#     chat_id = message.chat.id
#     print(msg.question,
#         [_.text for _ in msg.options],
#         msg.type,
#         msg.correct_option_id,
#         msg.is_anonymous)
#     await message.answer(str(msg) + str(chat_id), parse_mode="Markdown")
#     await message.answer_poll(
#         question=msg.question,
#         options=[_.text for _ in msg.options],
#         type=msg.type,
#         correct_option_id=msg.correct_option_id,
#         is_anonymous=msg.is_anonymous
#     )

# @router.poll_answer()
# async def poll_answer_handler(poll: PollAnswer):
#     answer_ids = poll.option_ids # list of answers
#     user_id = poll.user.id
#     poll_id = poll.poll_id

#     print(user_id)

# @router.message(Command("Проверка"))
# async def check_handler(message: Message):
#     global polls
#     await message.answer()