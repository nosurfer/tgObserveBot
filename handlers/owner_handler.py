import main

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, PollAnswer

from filters.own_filters import IsOwner, ChatTypeFilter
from utils.kbrd import get_keyboard, get_inline_keyboard

from database.core import Database

router = Router()
router.message.filter(ChatTypeFilter("private"), IsOwner())


@router.message(Command("owner"))
async def owner_handler(message: Message):
    ikbrd = get_inline_keyboard(
        ("Дать права админа", "plus_admin", None)
    )
    await message.answer("Панель разработчика", reply_markup=ikbrd)

# @router.callback_query(F.data == "plus_admin")
