from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton


def get_keyboard(*buttons: str, placeholder: str = None, request_contact: int = None, request_location: int = None, sizes: tuple[int] = (2,)):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона"
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(buttons, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)


def get_inline_keyboard(*buttons: tuple[str, str, str], sizes: tuple[int] = (2,)):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_inline_keyboard(
        ("button_name", "data", "url"),
        sizes=(2, 2, 1)
        )
    '''
    
    keyboard = InlineKeyboardBuilder()

    for index, tuple_value in enumerate(buttons, start=0):
        text, data, url = tuple_value
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data, url=url))

    return keyboard.adjust(*sizes).as_markup()