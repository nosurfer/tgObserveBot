# https://www.youtube.com/watch?v=55w2QpPGC-E&ab_channel=PythonHubStudio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery, PollAnswer, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from filters.own_filters import ChatTypeFilter, IsAdmin, IsOwner

from utils.kbrd import get_keyboard, get_inline_keyboard
from utils.states import PollState

router = Router()
router.message.filter(ChatTypeFilter("private"), IsOwner() or IsAdmin())

admin_kbrd = get_keyboard(
    "Создать опрос",
    "Закрыть панель",
    placeholder="Админ панель:",
    sizes=(2, 2, 1)
)


@router.message(StateFilter(None), Command("admin"))
async def admin_kbrd_handler(message: Message):
    await message.answer("Админ панель открыта", reply_markup=admin_kbrd)


@router.message(StateFilter(None), F.text.lower() == "создать опрос")
async def create_poll_handler(message: Message, state: FSMContext):
    poll_kbrd = get_keyboard("Отмена", placeholder="Создание опроса:")
    await message.answer("Отправьте опрос", reply_markup=poll_kbrd)
    await state.set_state(PollState.poll)


@router.message(PollState.poll, F.poll)
async def pollstate_poll_handler(message: Message, state: FSMContext):
    check_kbrd = get_inline_keyboard(
        ("✅Да", "да", None),
        ("❌Нет", "нет", None),
    )
    await state.update_data(poll = message.poll)
    await message.answer(str(message.poll))
    await message.answer("Вы уверены что хотите отправить этот опрос?", reply_markup=check_kbrd)
    await state.set_state(PollState.check)


@router.callback_query(PollState.check)
async def pollstate_check_handler(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "да":
        poll = await state.get_data()

        await callback_query.message.answer(str(poll))

        await callback_query.message.answer("Опрос отправлен", reply_markup=admin_kbrd)
        await callback_query.answer(text="Опрос отправлен")
        await state.clear()
    elif callback_query.data == "нет":
        current_state = await state.get_state()
        
        previous = None
        for step in PollState.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await callback_query.answer("Отправьте опрос ещё раз")
                await callback_query.message.answer("Отправьте опрос ещё раз")
                return
            previous = step
        

# @router.message(PollState.check, F.text.casefold() == "да")
# async def pollstate_check_handler(message: Message, state: FSMContext):
#     data = await state.get_data()
#     await message.answer(str(data))
#     await state.clear()
#     await message.answer("Опрос был отправлен", reply_markup=admin_kbrd)


# @router.message(PollState.check, F.text.casefold() == "нет")
# async def pollstate_back__handler(message: Message, state: FSMContext):
#     current_state = await state.get_state()

#     if current_state == PollState.poll:
#         await message.answer("Действие не возможно")
#         return
    
#     previous = None
#     for step in PollState.__all_states__:
#         if step.state == current_state:
#             await state.set_state(previous)
#             await message.answer("Отправьте опрос ещё раз", reply_markup=poll_kbrd)
#             return
#         previous = step


@router.message(StateFilter("*"), F.text.casefold() == "назад")
async def back_state_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == PollState.poll:
        await message.answer("Действие не возможно")
        return
    
    previous = None
    for step in PollState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer("Отправьте запрос ещё раз")
            return
        previous = step


@router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_state_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Все действия были отменены", reply_markup=admin_kbrd)


# @router.message(F.poll)
# async def read_poll_handler(message: Message):
#     global polls
#     polls.append(message.poll.poll_id)
#     msg = message.poll
#     chat_id = message.chat.id
#     print(msg.question,
#         [_.text for _ in msg.options],
#         msg.type,
#         msg.correct_option_id,
#         msg.is_anonymous)
#     await message.answer(str(msg) + str(chat_id), parse_mode="Markdown")
#     await message.answer_poll(
#         question=msg.question,
#         options=[_.text for _ in msg.options],
#         type=msg.type,
#         correct_option_id=msg.correct_option_id,
#         is_anonymous=msg.is_anonymous
#     )

# @router.poll_answer()
# async def poll_answer_handler(poll: PollAnswer):
#     answer_ids = poll.option_ids # list of answers
#     user_id = poll.user.id
#     poll_id = poll.poll_id

#     print(user_id)

# @router.message(Command("Проверка"))
# async def check_handler(message: Message):
#     global polls
#     await message.answer()

@router.message(StateFilter(None), F.text.lower() == "закрыть панель")
async def close_kbrd_handler(message: Message):
    await message.answer("Панель закрыта", reply_markup=ReplyKeyboardRemove())