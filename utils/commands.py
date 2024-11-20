from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

import main
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
    for user_value in await main.db.selectUser():
        user_id, username = user_value
        await bot.set_my_commands(commands=user_commands, scope=BotCommandScopeChat(chat_id=user_id))
    for user_value in await main.db.searchAdmin():
        group_id, user_id = user_value
        await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=user_id))
    for user_id in main.owners:
        await bot.set_my_commands(commands=owner_commands, scope=BotCommandScopeChat(chat_id=user_id))