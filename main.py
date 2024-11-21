import sys
import asyncio
import logging
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers import user_handler, admin_handler, owner_handler, bot_handler

from utils.commands import setCommands
from database.core import Database

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
owners = [1149076542, 1229865646]

bot = Bot(token=BOT_TOKEN)
db = Database()

async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(
        user_handler.router,
        admin_handler.router,
        owner_handler.router,
        bot_handler.router
    )
    
    await setCommands(bot)
    await dp.start_polling(bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main())