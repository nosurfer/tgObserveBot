# https://www.youtube.com/watch?v=55w2QpPGC-E&ab_channel=PythonHubStudio
import main

from aiogram import Router, F, FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, PollAnswer, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from filters.own_filters import ChatTypeFilter, IsAdmin, IsOwner
from database.core import Database
from utils.kbrd import get_keyboard, get_inline_keyboard
from utils.states import PollState

router = Router()
router.message.filter(ChatTypeFilter("private"), IsOwner() or IsAdmin())


@router.message(Command("admin"))
async def admin_kbrd_handler(message: Message):
    text = """*Админ панель*

Для того, чтобы опубликовать опрос, просто оптравьте мне опрос, который необходимо отправить в группу!
Для побликации сообщения в личные сообщения студентам, просто отправьте сообщение!"""
    await message.answer(text, parse_mode="Markdown")


@router.message(F.text)
async def mailing_handler(message: Message, state: FSMContext):
    ikbrd = get_inline_keyboard(("✅Да", "yes_mail", None))
    await state.update_data(msg = message.text)
    await message.reply("Вы уверены что хотите отправить всем это сообщение?", reply_markup=ikbrd)
    await state.set_state(PollState.poll)


@router.callback_query(PollState.poll, F.data == "yes_mail")
async def poll_check_handler(callback_query: CallbackQuery):
    global mail
    await callback_query.answer(text="Обработка результата")
    await callback_query.message.delete()
    users = await Database.selectUser()
    admins = await Database.selectAdmin()
    print(admins)
    for user_id, user_name in users.items():
        if user_id not in admins:
            print(user_id)
            await main.bot.send_message(user_id, mail, parse_mode="Markdown")
    await callback_query.message.answer("Сообщение отправлено")


@router.message(F.poll)
async def poll_handler(message: Message):
    global poll
    check_kbrd = get_inline_keyboard(("✅Да", "yes_poll", None))
    poll = str(message.poll)
    await message.answer(poll)
    await message.answer("Вы уверены что хотите отправить этот опрос?", reply_markup=check_kbrd)


@router.callback_query(F.data == "yes_poll")
async def poll_check_handler(callback_query: CallbackQuery):
    global poll
    await callback_query.answer(text="Обработка результата")
    await callback_query.message.delete()
    await callback_query.message.answer(poll)
    await callback_query.message.answer("Опрос отправлен")