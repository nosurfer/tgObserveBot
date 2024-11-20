import asyncio

from aiogram.filters import Filter
from aiogram.types import Message

import main

class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str] | str) -> None:
        if isinstance(chat_types, str):
            chat_types = [chat_types]
        self.chat_types = chat_types
    
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return await main.db.checkValue(user_id=message.from_user.id, is_admin=True)


class IsOwner(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in main.owners