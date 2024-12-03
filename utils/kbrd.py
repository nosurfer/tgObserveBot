from aiogram.types import KeyboardButton, KeyboardButtonRequestChat
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton


def get_keyboard(*buttons: str, sizes: tuple[int] = (2,)):
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


def get_inline_keyboard(*buttons: dict, sizes: tuple[int] = (2,)):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_inline_keyboard(
        ({"text": "Button 1", 
        "callback_data": "asdf",
        "url": "https://asdf.ru"},
        "request_chat": ...),
        sizes=(2, 2, 1)
        )
    '''
    
    keyboard = InlineKeyboardBuilder()

    for button in buttons:
        if "request_chat" in button:
            request_chat = button.pop("request_chat")
            keyboard.add(InlineKeyboardButton(**button, request_chat=request_chat))
        else:
            keyboard.add(InlineKeyboardButton(**button))

    return keyboard.adjust(*sizes).as_markup()