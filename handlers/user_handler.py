from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Poll, PollAnswer

from database.core import Database

# https://www.youtube.com/watch?v=Ipvmq1nkLlk&list=PLEYdORdflM3lkbY2N9mH8pfH_-wPR9q9R&index=5&ab_channel=%D0%A4%D1%81%D0%BE%D0%BA%D0%B8

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:    
    user_id = message.from_user.id
    user_name = "@" + str(message.from_user.username) or message.from_user.first_name
    mention = "["+user_name+"](tg://user?id="+str(user_id)+")"
    
    title = """Простой и удобный телеграм бот для проведения опросов.\
        Создаёт опросы, собирает ответы и предоставляет статистику по результатам.\n\n"""

    try:
        user_group_id = message.text.split()[1]
    except:
        user_group_id = 0

    if await Database.checkUser(user_id):
        msg = f"{mention}, Вы уже были зарегистрированы.\n\n"
    else:
        await Database.insertUser(user_id, user_name)
        msg = f"{mention}, Вы были добавлены в систему.\n\n"
    
    if not await Database.checkUserGroup(user_id, user_group_id):
        if await Database.checkGroup(user_group_id):
            await Database.insertUserGroup(user_id, user_group_id)
    
    msg += "Привязанные группы:\n"
    user_groups = await Database.selectUserGroup(user_id=user_id)
    if user_groups:
        for g_id, u_id, is_a in user_groups:
            group = await Database.selectGroup(g_id)
            msg += " - " + group[0][1] + "\n"
    await message.answer(title + msg, parse_mode="Markdown")