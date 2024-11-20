from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ChatMemberUpdated

from utils.kbrd import get_inline_keyboard

import main

router = Router()

@router.my_chat_member()
async def bot_group_member_status(update: ChatMemberUpdated):
    chat_id = update.chat.id
    chat_name = update.chat.title or ""
    status = update.new_chat_member.status

    msg = f"Это простой и удобный телеграм бот для проведения опросов.\
            Создаёт опросы, собирает ответы и предоставляет статистику по результатам.\n\n"
    
    if status == "member":
        admins = await main.bot.get_chat_administrators(chat_id=chat_id)
        admins = [_.user.id for _ in admins]
        await main.db.insertAdmin(chat_id, *admins)
        bot_info = await main.bot.get_me()
        kbrd = get_inline_keyboard(("Зарегистрироваться", None, f"https://t.me/{bot_info.username}?start={chat_id}"))

        await main.db.insertGroup(chat_id, chat_name)
        await update.answer(msg + "***Dev by @Sirius_Real, @ownnickname***", parse_mode="Markdown", reply_markup=kbrd)
    else:
        await main.db.deleteGroup(chat_id, chat_name)
        