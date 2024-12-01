from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, PollAnswer

from utils.kbrd import get_keyboard, get_inline_keyboard

from database.core import Database

# async def users_handler(callback_query: CallbackQuery):
#     await callback_query.answer(text="Обработка результата")
#     users = await Database.selectUser()
#     text = """"""
#     await callback_query.message.answer()