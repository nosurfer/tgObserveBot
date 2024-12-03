from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, PollAnswer, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


from filters.own_filters import ChatTypeFilter, IsAdmin, IsOwner

from utils.kbrd import get_keyboard, get_inline_keyboard

router = Router()
router.message.filter(ChatTypeFilter(["group", "supergroup"]), IsOwner() or IsAdmin())

poll = None

@router.message(F.poll)
async def poll_handler(message: Message):
    global poll
    poll = message.poll
    if poll.question.startswith("+"):
        await message.delete()
        if poll.type == "quiz":
            await message.answer("Увы, на данный момент бот не поддерживает опросы типа \"Квиз\"")
            return
        await message.answer(str(poll))
        await message.answer_poll(
            question=poll.question[1:],
            options=[_.text for _ in poll.options],
            type=poll.type,
            is_anonymous=poll.is_anonymous,
            allows_multiple_answers=poll.allows_multiple_answers,
            question_entities=poll.question_entities,
            open_period=poll.open_period,
            close_date=poll.close_date
        )