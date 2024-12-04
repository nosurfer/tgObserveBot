from aiogram.types import KeyboardButton, KeyboardButtonRequestChat
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton


def get_keyboard(*buttons: dict, placeholder = None, sizes: tuple[int] = (2,)):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            {...}
            placeholder="Что вас интересует?",
            sizes=(2, 2, 1)
        )
    '''
    
    keyboard = ReplyKeyboardBuilder()

    for button in buttons:
        if "request_chat" in button:
            request_chat = button.pop("request_chat")
            keyboard.add(KeyboardButton(**button, request_chat=KeyboardButtonRequestChat(**request_chat)))
        else:
            keyboard.add(KeyboardButton(**button))

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
        keyboard.add(InlineKeyboardButton(**button))

    return keyboard.adjust(*sizes).as_markup()