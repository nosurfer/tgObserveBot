from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Poll, PollAnswer

from database.core import Database

# https://www.youtube.com/watch?v=Ipvmq1nkLlk&list=PLEYdORdflM3lkbY2N9mH8pfH_-wPR9q9R&index=5&ab_channel=%D0%A4%D1%81%D0%BE%D0%BA%D0%B8

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    try:
        group_id = message.text.split()[1]
    except:
        group_id = 0
        
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name
    mention = "[@"+user_name+"](tg://user?id="+str(user_id)+")"
    
    title = """Простой и удобный телеграм бот для проведения опросов.\
        Создаёт опросы, собирает ответы и предоставляет статистику по результатам.\n\n"""
    
    if await Database.checkUser(user_id):
        await message.answer("ты в базе)))")
    else:
        await message.answer("ты не базе(")
        await Database.insertUser(user_id, user_name)

    message.answer(await Database.selectUser())


    # проверка есть ли пользователь в системе
    # да - дальше
    # нет - добавить

    # проверка есть ли у пользователя такая группа
    # да - закончить проверку
    # нет - проверить есть ли такая у бота

    # проверка у бота
    # есть - добавить пользователю
    # отуствует - сказать об ошибке

    # if not await Database.checkUser(user_id):
    #     await Database.insertUser(user_id, user_name)
    #     msg = f"{mention}, Вы были добавлены в систему.\n\n"
    # else:
    #     msg = f"{mention}, Вы уже были зарегистрированы.\n\n"
    
    # if not await Database.checkUserGroup(user_id, group_id):
    #     if await Database.checkGroup(group_id):
    #         await Database.insertUserGroup(user_id, group_id)
    
    # msg += "Привязанные группы:\n"
    # groups = await Database.selectUserGroup(user_id)
    # for index, i in enumerate(groups, start=1):
    #     group_name = await Database.selectGroup(*i)
    #     msg += f"{index}) " + group_name[0][0] + "\n"
    
    # await message.answer(title + msg + "\n***Dev by @Sirius_Real, @ownnickname***", parse_mode="Markdown")


    # if await Database.checkUser(user_id):
    #     msg += f"{mention}, вы уже прошли регистрацию.\n\n***Dev by @Sirius_Real, @ownnickname***"
    #     await message.answer(msg, parse_mode="Markdown")
    # else:
    #     user_fullname = ("@" + message.from_user.username) or (message.from_user.first_name or "" + " " + message.from_user.last_name or "")
    #     await Database.insertUser(user_id, user_fullname)
    #     msg += f"{mention}, вы были успешно зарегистрированы!\n\n***Dev by @Sirius_Real, @ownnickname***"
    #     await message.answer(msg, parse_mode="Markdown")