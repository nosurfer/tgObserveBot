from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ChatMemberUpdated

from utils.kbrd import get_inline_keyboard

from database.core import Database
import main

router = Router()

@router.my_chat_member()
async def bot_group_member_status(update: ChatMemberUpdated):
    chat_id = update.chat.id
    chat_name = update.chat.title or ""
    status = update.new_chat_member.status

    msg = f"Это простой и удобный телеграм бот для проведения опросов.\
            Создаёт опросы, собирает ответы и предоставляет статистику по результатам.\n\n"
    if status == "member" and update.new_chat_member.user.id == main.bot.id:
        admins = [
            (_.user.id, _.user.username or _.user.first_name) 
            for _ in await 
            main.bot.get_chat_administrators(chat_id=chat_id)
        ]
        await Database.insertGroup(group_id=chat_id, group_name=chat_name)
        for admin in admins:
            admin_id, admin_name = admin
            if not await Database.checkUser(user_id=admin_id):
                await Database.insertUser(user_id=admin_id, user_name=admin_name)
            await Database.insertUserGroup(user_id=admin_id, group_id=chat_id)
            await Database.updateAdmin(group_id=chat_id, user_id=admin_id, value=True)
        bot_info = await main.bot.get_me()
        kbrd = get_inline_keyboard({"text": "Зарегистрироваться", "url": f"https://t.me/{bot_info.username}?start={chat_id}"})

        await update.answer(msg, parse_mode="Markdown", reply_markup=kbrd)
    elif status in ["left", "kicked"] and update.new_chat_member.user.id == main.bot.id:
        await Database.deleteGroup(group_id=chat_id)