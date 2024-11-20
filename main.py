import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import user_handler, admin_handler, owner_handler, bot_handler

from utils.commands import setCommands
from utils.sql import InteractionWithDB

from config import BOT_TOKEN

owners = [1149076542, 1229865646]
# owners = [1229865646]

bot = Bot(token=BOT_TOKEN)
db = InteractionWithDB()


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