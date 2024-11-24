from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

from database.core import Database
from base_config import env_values


# https://www.youtube.com/watch?v=HRAzGBdwCkw&ab_channel=NZTCODER

async def setCommands(bot: Bot):
    user_commands = [
        BotCommand(
            command="start",
            description="Краткое описание бота"
        )
    ]

    admin_commands = [
        BotCommand(
            command="start",
            description="Краткое описание бота"
        ),
        BotCommand(
            command="admin",
            description="Открыть админ панель"
        )
    ]

    owner_commands = [
        BotCommand(
            command="start",
            description="Краткое описание бота"
        ),
        BotCommand(
            command="admin",
            description="Открыть админ панель"
        ),
        BotCommand(
            command="owner",
            description="Открыть панель разработчика"
        )
    ]

    await bot.set_my_commands(commands=user_commands, scope=BotCommandScopeAllPrivateChats())
    try:
        for user_id, user_name in await Database.selectUser():
            print(user_id, user_name)
            await bot.set_my_commands(commands=user_commands, scope=BotCommandScopeChat(chat_id=user_id))
    except:
        pass
    try:
        for group_id, user_id in await Database.selectAdmin():
            print(user_id, user_name)
            await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=user_id))
    except:
        pass
    for user_id in env_values["OWNERS"].split(";"):
        await bot.set_my_commands(commands=owner_commands, scope=BotCommandScopeChat(chat_id=user_id))