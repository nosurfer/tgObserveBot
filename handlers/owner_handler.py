from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, PollAnswer

from filters.own_filters import IsOwner, ChatTypeFilter
from utils.kbrd import get_keyboard

import main

router = Router()
router.message.filter(ChatTypeFilter("private"), IsOwner())

KB = get_keyboard(
    "Закрыть панель",
    placeholder="Панель разработчика:",
    sizes=(2, 2, 1)
)


@router.message(StateFilter(None), Command("owner"))
async def admin_kbrd_handler(message: Message):
    await message.answer("Панель разработчика открыта", reply_markup=KB)


# @router.message(F.text.lower() == "Вывести таблицу")
# async def admin_kbrd_handler(message: Message):
#     await main.db.clearTable("users")
#     await message.answer("Таблица успешно очищина")


@router.message(F.text.lower() == "закрыть панель")
async def close_kbrd_handler(message: Message):
    await message.answer("Панель разработчика закрыта", reply_markup=ReplyKeyboardRemove())