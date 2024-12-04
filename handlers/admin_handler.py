# https://www.youtube.com/watch?v=55w2QpPGC-E&ab_channel=PythonHubStudio
from main import bot

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, PollAnswer, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from filters.own_filters import ChatTypeFilter, IsAdmin, IsOwner
from database.core import Database
from utils.kbrd import get_keyboard, get_inline_keyboard
from utils.states import PollState, GroupState

router = Router()
router.message.filter(ChatTypeFilter("private"), IsOwner() or IsAdmin())


@router.message(Command("admin"))
async def admin_ikbrd_handler(message: Message):
    ikbrd = get_inline_keyboard(
        {"text": "👥 Выбрать группу","callback_data": "admin:select_group", "request_chat": {"request_id": 1, "chat_is_channel": False}},
        {"text": "✉️ Сделать рассылку", "callback_data": "admin:mailing"},
        {"text": "📊 Создать опрос", "callback_data": "admin:poll"},
        sizes=(1,)
    )
    text = """*Админ панель*"""
    
    await message.answer(text, parse_mode="Markdown", reply_markup=ikbrd)


# @router.callback_query(F.data == "admin:back")
# async def admin_ikbrd_reply_handler(callback_query: CallbackQuery):
#     ikbrd = get_inline_keyboard(
#         {"text": "👥 Выбрать группу","callback_data": "admin:select_group", "request_chat": {"request_id": 1, "chat_is_channel": False}},
#         {"text": "✉️ Сделать рассылку", "callback_data": "admin:mailing"},
#         {"text": "📊 Создать опрос", "callback_data": "admin:poll"},
#         sizes=(1,)
#     )

#     text = """*Админ панель*"""
#     await callback_query.message.delete()
#     await callback_query.message.answer(text, parse_mode="Markdown", reply_markup=ikbrd)

@router.callback_query(F.data == "admin:select_group")
async def group_selector_handler(callback_query: CallbackQuery, state: FSMContext):
    ikbrd = get_inline_keyboard(
        {"text": "Установить группу", "callback_data": "group:select"},
        {"text": "Вернуться назад", "callback_data": "admin:back"}
    )
    kbrd = get_keyboard(
        {"text": "Выберите группу", "request_chat": {"request_id": 1, "chat_is_channel": False}},
        placeholder="Выберите группу для взаимодействия:",
        sizes=(1,)
    )

    current_group = await state.get_data() or "Не выбрана"

    group_list = ""
    groups = await Database.selectUserGroup(callback_query.from_user.id)
    for index, group_id, user_id, is_admin in enumerate(groups, start=1):
        group_id, group_name = await Database.selectGroup(group_id)
        group_list += f"{index}) {group_name}\n"

    await callback_query.message.answer(
        f"Установите группу, для дальнейшего взаимодействия с ней и её участниками\n\nВаши группы:\n{group_list}\nТекущая группа: {current_group}",
        reply_markup=kbrd)



@router.message(F.text == "asdf")
async def mailing_handler(message: Message, state: FSMContext):
    await state.set_state(PollState.poll)
    await state.update_data(txt = message.text)
    await state.finish()







@router.message(F.text)
async def mailing_handler(message: Message, state: FSMContext):
    ikbrd = get_inline_keyboard({"text": "✅Да", "callback_data": "yes_mail"})
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








# @router.inline_handler()
# async def inline_handler(query: InlineQuery):
#     # Create an inline button with a "request_chat" parameter
#     inline_keyboard = InlineKeyboardMarkup().add(
#         InlineKeyboardButton(
#             text="Select a Chat",
#             request_chat=types.KeyboardButtonRequestChat(
#                 request_id=1,  # Unique request ID
#                 chat_is_channel=False,  # Request user chats (False for groups, True for channels)
#                 chat_is_forum=False,  # If you want to restrict to groups with forum
#                 user_administrator_rights=None,  # Filter only groups where the bot has admin rights
#                 bot_administrator_rights=None,  # Filter groups where a bot is admin
#                 member_count=None,  # Minimum number of members required in the chat
#             )
#         )
#     )

#     # InlineQueryResultArticle with the chat request button
#     item = InlineQueryResultArticle(
#         id="1",
#         title="Request a Chat",
#         input_message_content=InputTextMessageContent(
#             message_text="Please select a chat using the button below."
#         ),
#         reply_markup=inline_keyboard,
#     )

#     await query.answer([item], cache_time=1)